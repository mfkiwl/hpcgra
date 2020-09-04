from math import ceil, log

from veriloggen import *

from utils import initialize_regs, bits


class Components:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.cache = {}

    def create_register_pipeline(self):
        name = 'reg_pipe'
        if name in self.cache.keys():
            return self.cache[name]

        m = Module('reg_pipe')
        num_stages = m.Parameter('num_register', 1)
        data_width = m.Parameter('width', 16)

        clk = m.Input('clk')
        en = m.Input('en')
        rst = m.Input('rst')
        data_in = m.Input('in', data_width)
        data_out = m.Output('out', data_width)

        regs = m.Reg('regs', data_width, num_stages)
        i = m.Integer('i')
        m.EmbeddedCode('')
        data_out.assign(regs[num_stages - 1])
        m.Always(Posedge(clk))(
            If(rst)(
                regs[0](0),
            ).Else(
                If(en)(
                    regs[0](data_in),
                    For(i(1), i < num_stages, i.inc())(
                        regs[i](regs[i - 1])
                    )
                )
            )
        )

        initialize_regs(m)
        self.cache[name] = m
        return m

    def create_multiplexer(self, size):
        name = 'multiplexer_%d' % size
        if name in self.cache.keys():
            return self.cache[name]

        m = Module('multiplexer_%d' % size)
        width = m.Parameter('width', 8)
        select = m.Input('sel', bits(size))
        inputs = [m.Input('in%d' % i, width) for i in range(size)]
        output = m.Output('out', width)
        wires = m.Wire('aux', width, size)

        for i in range(size):
            wires[i].assign(inputs[i])

        output.assign(wires[select])
        self.cache[name] = m
        return m

    def create_memory(self):
        name = 'memory'
        if name in self.cache.keys():
            return self.cache[name]

        m = Module(name)
        init_file = m.Parameter('init_file', 'mem_file.txt')
        data_width = m.Parameter('data_width', 32)
        addr_width = m.Parameter('addr_width', 8)
        clk = m.Input('clk')
        we = m.Input('we')
        re = m.Input('re')

        raddr = m.Input('raddr', addr_width)
        waddr = m.Input('waddr', addr_width)
        din = m.Input('din', data_width)
        dout = m.OutputReg('dout', data_width)

        m.EmbeddedCode('(* ramstyle = "AUTO, no_rw_check" *) reg  [data_width-1:0] mem[0:2**addr_width-1];')
        m.EmbeddedCode('/*')
        mem = m.Reg('mem', data_width, Power(2, addr_width))
        m.EmbeddedCode('*/')

        m.Always(Posedge(clk))(
            If(we)(
                mem[waddr](din)
            ),
            If(re)(
                dout(mem[raddr])
            )
        )
        m.EmbeddedCode('//synthesis translate_off')

        i = m.Integer('i')
        m.Initial(
            dout(0),
            For(i(0), i < Power(2, addr_width), i.inc())(
                mem[i](0)
            ),
            Systask('readmemb', init_file, mem)
        )
        m.EmbeddedCode('//synthesis translate_on')
        self.cache[name] = m
        return m

    def create_elastic_pipeline(self, max_latency):
        name = 'elastic_pipeline_%d' % max_latency
        if name in self.cache.keys():
            return self.cache[name]

        max_latency_bits = bits(max_latency + 1)
        m = Module(name)
        width = m.Parameter('width', 8)
        if max_latency > 0:
            clk = m.Input('clk')
            latency = m.Input('latency', max_latency_bits)
            din = m.Input('in', width)
            dout = m.Output('out', width)

            shift_reg = m.Reg('shift_reg', width, 3 * max_latency)
            i = m.Integer('i')
            m.Always(Posedge(clk))(
                shift_reg[0](din),
                For(i(1), i < 3 * max_latency, i.inc())(
                    shift_reg[i](shift_reg[i - 1])
                )
            )
            mux = self.create_multiplexer(max_latency + 1)
            con = [('sel', latency), ('in0', din)]
            con += [('in%d' % j, shift_reg[(j * 3) - 1]) for j in range(1, max_latency + 1)]
            con.append(('out', dout))
            params = [('width', width)]
            m.Instance(mux, 'mux' % i, params, con)
        else:
            din = m.Input('in', width)
            dout = m.Output('out', width)
            dout.assign(din)

        initialize_regs(m)
        self.cache[name] = m
        return m

    def create_switch_box(self, num_in, num_out):
        name = 'switch_%d_%d' % (num_in, num_out)
        if name in self.cache.keys():
            return self.cache[name]

        m = Module(name)
        width = m.Parameter('width', 16)

        ports_in = []
        ports_out = []

        bits = int(ceil(log(num_in, 2)) * num_out)
        step = int(ceil(log(num_in, 2)))

        m.Input('sel', bits)

        for i in range(num_in):
            ports_in.append(m.Input('in%d' % i, width))

        for i in range(num_out):
            ports_out.append(m.Output('out%d' % i, width))

        mux = self.create_multiplexer(num_in)
        ports_cross = m.get_ports()
        for i in range(num_out):
            p = []
            for j in range(num_in):
                p.append(('in%d' % j, ports_cross['in%d' % j]))
            start = -(step * num_out) + (i * step)
            stop = -(step * num_out - 1) + (i * step) + step - 1
            if start != 0 and stop != 0:
                p.append(('sel', ports_cross['sel'][start:stop]))
            elif start == 0:
                p.append(('sel', ports_cross['sel'][:stop]))
            else:
                p.append(('sel', ports_cross['sel'][start:]))

            p.append(('out', ports_cross['out%d' % i]))
            m.Instance(mux, ('mux%d' % i), params=m.connect_params(mux), ports=p)

        self.cache[name] = m
        return m

    def create_router(self, routes, num_in, num_out):
        name = 'route_%d_%dx%d' % (routes, num_in, num_out)
        if name in self.cache.keys():
            return self.cache[name]
        m = Module(name)
        width = m.Parameter('width', 16)

        if routes == 0:
            in0 = m.Input('in0', width)
            outputs = [m.Output('out%d' % i, width) for i in range(num_out)]
            for o in outputs:
                o.assign(in0)

        elif routes == 1:
            mux = self.create_multiplexer(num_in)
            p = mux.get_ports()
            sel_in = m.Input('sel_in', p['sel'].width)
            inputs = [('in%d' % i, m.Input('in%d' % i, width)) for i in range(num_in)]
            outputs = [('out%d' % i, m.Output('out%d' % i, width)) for i in range(num_out)]
            mux_out = m.Wire('mux_out', width)
            m.Instance(mux, mux.name, [('width', width)], [('sel', sel_in)] + inputs + [('out', mux_out)])
            for o in outputs:
                o[1].assign(mux_out)
        elif routes >= num_out:
            switch_in = self.create_switch_box(num_in, num_out)
            p = switch_in.get_ports()
            sel_in = m.Input('sel_in', p['sel'].width)
            inputs = [('in%d' % i, m.Input('in%d' % i, width)) for i in range(num_in)]
            outputs = [('out%d' % i, m.Output('out%d' % i, width)) for i in range(num_out)]
            m.Instance(switch_in, switch_in.name, [('width', width)], [('sel', sel_in)] + inputs + outputs)
        else:
            switch_in = self.create_switch_box(num_in, routes)
            switch_out = self.create_switch_box(routes, num_out)
            p_in = switch_in.get_ports()
            p_out = switch_out.get_ports()
            sel_in = m.Input('sel_in', p_in['sel'].width)
            sel_out = m.Input('sel_out', p_out['sel'].width)
            inputs = [('in%d' % i, m.Input('in%d' % i, width)) for i in range(num_in)]
            outputs = [('out%d' % i, m.Output('out%d' % i, width)) for i in range(num_out)]
            sin_sout_out = [('out%d' % i, m.Wire('sin_sout%d' % i, width)) for i in range(routes)]
            sin_sout_in = [('in%d' % i, sin_sout_out[i][1]) for i in range(routes)]
            m.Instance(switch_in, switch_in.name, [('width', width)], [('sel', sel_in)] + inputs + sin_sout_out)
            m.Instance(switch_out, switch_out.name, [('width', width)], [('sel', sel_out)] + sin_sout_in + outputs)

        self.cache[name] = m
        return m
