from math import ceil

from veriloggen import *
from veriloggen.types.util import *

from src.hw.utils import initialize_regs, bits


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
            Systask('readmemh', init_file, mem)
        )
        m.EmbeddedCode('//synthesis translate_on')
        self.cache[name] = m
        return m

    def create_fifo(self):
        m = Module('fifo')
        FIFO_WIDTH = m.Parameter('FIFO_WIDTH', 32)
        FIFO_DEPTH_BITS = m.Parameter('FIFO_DEPTH_BITS', 8)
        FIFO_ALMOSTFULL_THRESHOLD = m.Parameter('FIFO_ALMOSTFULL_THRESHOLD', Power(2, FIFO_DEPTH_BITS) - 4)
        FIFO_ALMOSTEMPTY_THRESHOLD = m.Parameter('FIFO_ALMOSTEMPTY_THRESHOLD', 2)

        clk = m.Input('clk')
        rst = m.Input('rst')
        we = m.Input('we')
        din = m.Input('din', FIFO_WIDTH)
        re = m.Input('re')
        valid = m.OutputReg('valid')
        dout = m.OutputReg('dout', FIFO_WIDTH)
        empty = m.OutputReg('empty')
        almostempty = m.OutputReg('almostempty')
        full = m.OutputReg('full')
        almostfull = m.OutputReg('almostfull')
        count = m.OutputReg('count', FIFO_DEPTH_BITS + 1)

        rp = m.Reg('rp', FIFO_DEPTH_BITS)
        wp = m.Reg('wp', FIFO_DEPTH_BITS)
        mem = m.Reg('mem', FIFO_WIDTH, Power(2, FIFO_DEPTH_BITS))

        m.Always(Posedge(clk))(
            If(rst)(
                empty(Int(1, 1, 2)),
                almostempty(Int(1, 1, 2)),
                full(Int(0, 1, 2)),
                almostfull(Int(0, 1, 2)),
                rp(0),
                wp(0),
                count(0)
            ).Else(
                Case(Cat(we, re))(
                    When(Int(3, 2, 2))(
                        rp(rp + 1),
                        wp(wp + 1),
                    ),
                    When(Int(2, 2, 2))(
                        If(~full)(
                            wp(wp + 1),
                            count(count + 1),
                            empty(Int(0, 1, 2)),
                            If(count == (FIFO_ALMOSTEMPTY_THRESHOLD - 1))(
                                almostempty(Int(0, 1, 2))
                            ),
                            If(count == Power(2, FIFO_DEPTH_BITS) - 1)(
                                full(Int(1, 1, 2))
                            ),
                            If(count == (FIFO_ALMOSTFULL_THRESHOLD - 1))(
                                almostfull(Int(1, 1, 2))
                            )
                        )

                    ),
                    When(Int(1, 2, 2))(
                        If(~empty)(
                            rp(rp + 1),
                            count(count - 1),
                            full(Int(0, 1, 2)),
                            If(count == FIFO_ALMOSTFULL_THRESHOLD)(
                                almostfull(Int(0, 1, 2))
                            ),
                            If(count == 1)(
                                empty(Int(1, 1, 2))
                            ),
                            If(count == FIFO_ALMOSTEMPTY_THRESHOLD)(
                                almostempty(Int(1, 1, 2))
                            )

                        )
                    ),
                    When()(

                    )

                )
            )
        )
        m.Always(Posedge(clk))(
            If(rst)(
                valid(Int(0, 1, 2))
            ).Else(
                valid(Int(0, 1, 2)),
                If(we == Int(1, 1, 2))(
                    mem[wp](din)
                ),
                If(re == Int(1, 1, 2))(
                    dout(mem[rp]),
                    valid(Int(1, 1, 2))
                )
            )
        )
        m.EmbeddedCode('//synthesis translate_off')
        m.Always(Posedge(clk))(
            If(we & full)(EmbeddedCode('$fatal("overflow");')),
            If(re & empty)(EmbeddedCode('$fatal("underflow");'))
        )
        m.EmbeddedCode('//synthesis translate_on')

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
            en = m.Input('en')
            latency = m.Input('latency', max_latency_bits)
            din = m.Input('in', width)
            dout = m.Output('out', width)
            shift_reg = m.Reg('shift_reg', width, 3 * max_latency)
            i = m.Integer('i')
            m.Always(Posedge(clk))(
                If(en)(
                    shift_reg[0](din),
                    For(i(1), i < 3 * max_latency, i.inc())(
                        shift_reg[i](shift_reg[i - 1])
                    )
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

    def create_control_conf(self, cgra_id, num_pe_io_in, num_pe_io_out, num_cicle_wait_conf_finish):
        name = 'cgra%d_control_conf' % cgra_id
        if name in self.cache.keys():
            return self.cache[name]

        m = Module(name)

        CONF_DATA_IN_WIDTH = m.Parameter('CONF_DATA_IN_WIDTH', 512)
        CONF_DATA_OUT_WIDTH = m.Parameter('CONF_DATA_OUT_WIDTH', 8)

        CONF_SIZE = m.Localparam('CONF_SIZE', Div(CONF_DATA_IN_WIDTH, CONF_DATA_OUT_WIDTH))

        clk = m.Input('clk')
        rst = m.Input('rst')
        start = m.Input('start')

        req_rd_data = m.Output('req_rd_data')
        rd_data = m.Input('rd_data', CONF_DATA_IN_WIDTH)
        rd_data_valid = m.Input('rd_data_valid')

        conf_out_bus = m.OutputReg('conf_out_bus', CONF_DATA_OUT_WIDTH)

        read_fifo_mask = m.OutputReg('read_fifo_mask', num_pe_io_in)
        write_fifo_mask = m.OutputReg('write_fifo_mask', num_pe_io_out)
        write_fifo_ignore = m.OutputReg('write_fifo_ignore', num_pe_io_out * 16)
        write_fifo_loop_ignore = m.OutputReg('write_fifo_loop_ignore', num_pe_io_out * 16)

        done = m.OutputReg('done')

        FSM_INIT_CTRL_IDLE = m.Localparam('FSM_INIT_CTRL_IDLE', 0)
        FSM_INIT_CTRL_INIT = m.Localparam('FSM_INIT_CTRL_INIT', 1)
        FSM_INIT_CTRL_INIT2 = m.Localparam('FSM_INIT_CTRL_INIT2', 2)
        FSM_INIT_CTRL_INIT3 = m.Localparam('FSM_INIT_CTRL_INIT3', 3)
        FSM_SEND_INIT_CONF_PE = m.Localparam('FSM_SEND_INIT_CONF_PE', 4)
        FSM_INIT_CTRL_REQ_DATA = m.Localparam('FSM_INIT_CTRL_REQ_DATA', 5)
        FSM_WAIT_ALL_CONF_FINISH = m.Localparam('FSM_WAIT_ALL_CONF_FINISH', 6)
        FSM_INIT_CONF_DONE = m.Localparam('FSM_INIT_CONF_DONE', 7)

        m.EmbeddedCode('')
        fsm_conf_ctrl = m.Reg('fsm_conf_ctrl', 4)
        fsm_conf_ctrl_next = m.Reg('fsm_conf_ctrl_next', 4)
        conf_req_data = m.Reg('conf_req_data')
        conf_cl = m.Reg('conf_cl', CONF_DATA_IN_WIDTH)
        qtd_conf = m.Reg('qtd_conf', 32)
        conf_data = m.Reg('conf_data', CONF_DATA_OUT_WIDTH)
        send_conf = m.Reg('send_conf')
        conf_counter = m.Reg('conf_counter', 32)
        conf_counter_cl = m.Reg('conf_counter_cl', 10)
        wait_counter = m.Reg('wait_counter', int(ceil(log2(num_cicle_wait_conf_finish))) + 1)

        m.EmbeddedCode('')

        req_rd_data.assign(conf_req_data)

        m.Always(Posedge(clk))(
            If(rst)(
                fsm_conf_ctrl(FSM_INIT_CTRL_IDLE),
                fsm_conf_ctrl_next(FSM_INIT_CTRL_IDLE),
                conf_req_data(0),
                send_conf(0),
                conf_counter(0),
                conf_counter_cl(CONF_SIZE),
                done(0),
                read_fifo_mask(0),
                write_fifo_mask(0),
                wait_counter(0)
            ).Else(
                conf_req_data(0),
                send_conf(0),
                done(0),
                Case(fsm_conf_ctrl)(
                    When(FSM_INIT_CTRL_IDLE)(
                        If(start)(
                            fsm_conf_ctrl(FSM_INIT_CTRL_REQ_DATA),
                            fsm_conf_ctrl_next(FSM_INIT_CTRL_INIT)
                        )
                    ),
                    When(FSM_INIT_CTRL_INIT)(
                        qtd_conf(conf_cl[0:18]),
                        read_fifo_mask(conf_cl[32:32 + num_pe_io_in]),
                        write_fifo_mask(conf_cl[96:96 + num_pe_io_out]),
                        fsm_conf_ctrl(FSM_INIT_CTRL_REQ_DATA),
                        fsm_conf_ctrl_next(FSM_INIT_CTRL_INIT2)
                    ),
                    When(FSM_INIT_CTRL_INIT2)(
                        write_fifo_ignore(conf_cl[0:num_pe_io_out * 16]),
                        fsm_conf_ctrl(FSM_INIT_CTRL_REQ_DATA),
                        fsm_conf_ctrl_next(FSM_INIT_CTRL_INIT3)
                    ),
                    When(FSM_INIT_CTRL_INIT3)(
                        write_fifo_loop_ignore(conf_cl[0:num_pe_io_out * 16]),
                        fsm_conf_ctrl(FSM_SEND_INIT_CONF_PE),
                    ),
                    When(FSM_SEND_INIT_CONF_PE)(
                        If(conf_counter >= qtd_conf)(
                            fsm_conf_ctrl(FSM_WAIT_ALL_CONF_FINISH)
                        ).Else(
                            If(conf_counter_cl < CONF_SIZE)(
                                conf_data(conf_cl[0:CONF_DATA_OUT_WIDTH]),
                                conf_cl(conf_cl[CONF_DATA_OUT_WIDTH:]),
                                send_conf(1),
                                conf_counter.inc(),
                                conf_counter_cl.inc(),
                            ).Else(
                                conf_counter_cl(Int(0, conf_counter_cl.width, 10)),
                                fsm_conf_ctrl(FSM_INIT_CTRL_REQ_DATA),
                                fsm_conf_ctrl_next(FSM_SEND_INIT_CONF_PE)
                            )
                        )
                    ),
                    When(FSM_INIT_CTRL_REQ_DATA)(
                        If(rd_data_valid)(
                            conf_cl(rd_data),
                            conf_req_data(1),
                            fsm_conf_ctrl(fsm_conf_ctrl_next),
                        )
                    ),
                    When(FSM_WAIT_ALL_CONF_FINISH)(
                        wait_counter.inc(),
                        If(wait_counter > num_cicle_wait_conf_finish)(
                            fsm_conf_ctrl(FSM_INIT_CONF_DONE),
                            done(1),
                        )
                    ),
                    When(FSM_INIT_CONF_DONE)(
                        If(~start)(
                            fsm_conf_ctrl(FSM_INIT_CTRL_IDLE)
                        )
                    )
                )
            )
        )

        m.Always(Posedge(clk))(
            If(rst)(
                conf_out_bus(0),
            ).Else(
                If(send_conf)(
                    conf_out_bus(conf_data),
                ).Else(
                    conf_out_bus(0)
                ),
            )
        )

        initialize_regs(m,
                        {'fsm_conf_ctrl': FSM_INIT_CTRL_IDLE,
                         'fsm_conf_ctrl_next': FSM_INIT_CTRL_IDLE,
                         'conf_counter_cl': CONF_SIZE})
        self.cache[name] = m

        return m

    def create_control_exec(self, cgra_id, num_pe_io_in, num_pe_io_out):
        name = 'cgra%d_control_exec' % cgra_id
        if name in self.cache.keys():
            return self.cache[name]
        m = Module(name)

        clk = m.Input('clk')
        rst = m.Input('rst')
        start = m.Input('start')

        read_fifo_mask = m.Input('read_fifo_mask', num_pe_io_in)
        write_fifo_mask = m.Input('write_fifo_mask', num_pe_io_out)
        write_fifo_ignore = m.Input('write_fifo_ignore', num_pe_io_out * 16)
        write_fifo_loop_ignore = m.Input('write_fifo_loop_ignore', num_pe_io_out * 16)

        available_pop = m.Input('available_pop', num_pe_io_in)
        available_push = m.Input('available_push', num_pe_io_out)

        read_fifo_done = m.Input('read_fifo_done', num_pe_io_in)
        write_fifo_done = m.Input('write_fifo_done', num_pe_io_out)

        en = m.Output('en')
        en_pop = m.Output('en_pop', num_pe_io_in)
        en_push = m.Output('en_push', num_pe_io_out)
        done = m.Output('done')

        FSM_IDLE = m.Localparam('FSM_IDLE', 0)
        FSM_PROCESS = m.Localparam('FSM_PROCESS', 1)
        FSM_DONE = m.Localparam('FSM_DONE', 2)

        m.EmbeddedCode('')

        fsm_state = m.Reg('fsm_state', 2)
        read_fifo_mask_r = m.Reg('read_fifo_mask_r', num_pe_io_in)
        write_fifo_mask_r = m.Reg('write_fifo_mask_r', num_pe_io_out)
        write_fifo_ignore_r = m.Reg('write_fifo_ignore_r', num_pe_io_out * 16)
        write_fifo_loop_ignore_r = m.Reg('write_fifo_loop_ignore_r', num_pe_io_out * 16)
        available_pop_masked = m.Reg('available_pop_masked', num_pe_io_in)
        available_push_masked = m.Reg('available_push_masked', num_pe_io_out)
        read_fifo_done_masked = m.Reg('read_fifo_done_masked', num_pe_io_in)
        write_fifo_done_masked = m.Reg('write_fifo_done_masked', num_pe_io_out)

        en_r = m.Reg('en_r')
        en_pop_r = m.Reg('en_pop_r', num_pe_io_in)
        en_push_r = m.Reg('en_push_r', num_pe_io_out)
        done_r = m.Reg('done_r')
        read_fifo_done_r = m.Reg('read_fifo_done_r', num_pe_io_in)
        write_fifo_done_r = m.Reg('write_fifo_done_r', num_pe_io_out)
        ignore_counter_out = m.Wire('ignore_counter_out', num_pe_io_out)
        en_counters = m.Reg('en_counter', num_pe_io_out)
        start_r = m.Reg('start_r')
        flag_initial = m.Reg('flag_initial')

        m.EmbeddedCode('')
        en.assign(en_r)
        en_pop.assign(en_pop_r)
        en_push.assign(And(ignore_counter_out, en_push_r))
        done.assign(done_r)

        m.Always(Posedge(clk))(
            If(rst)(
                start_r(Int(0, 1, 2))
            ).Else(
                start_r(Mux(start_r, start_r, start))
            )
        )

        m.Always(Posedge(clk))(
            read_fifo_mask_r(read_fifo_mask),
            write_fifo_mask_r(write_fifo_mask),
            write_fifo_ignore_r(write_fifo_ignore),
            write_fifo_loop_ignore_r(write_fifo_loop_ignore),
            read_fifo_done_r(read_fifo_done),
            write_fifo_done_r(write_fifo_done)
        )

        m.Always(Posedge(clk))(
            If(rst)(
                available_pop_masked(Repeat(Int(0, 1, 2), num_pe_io_in)),
                available_push_masked(Repeat(Int(0, 1, 2), num_pe_io_out)),
                read_fifo_done_masked(Repeat(Int(0, 1, 2), num_pe_io_in)),
                write_fifo_done_masked(Repeat(Int(0, 1, 2), num_pe_io_out))
            ).Elif(start_r)(
                available_pop_masked(Or(available_pop, Unot(read_fifo_mask_r))),
                available_push_masked(Or(available_push, Unot(write_fifo_mask_r))),
                write_fifo_done_masked(Or(write_fifo_done_r, Unot(write_fifo_mask_r))),
                read_fifo_done_masked(Or(read_fifo_done_r, Unot(read_fifo_mask_r)))
            ).Else(
                available_pop_masked(Repeat(Int(0, 1, 2), num_pe_io_in)),
                available_push_masked(Repeat(Int(0, 1, 2), num_pe_io_out)),
                read_fifo_done_masked(Repeat(Int(0, 1, 2), num_pe_io_in)),
                write_fifo_done_masked(Repeat(Int(0, 1, 2), num_pe_io_out))
            )
        )

        m.Always(Posedge(clk))(
            If(rst)(
                fsm_state(FSM_IDLE),
                done_r(Int(0, 1, 2)),
                en_r(Int(0, 1, 2)),
                en_pop_r(Repeat(Int(0, 1, 2), num_pe_io_in)),
                en_push_r(Repeat(Int(0, 1, 2), num_pe_io_in)),
                en_counters(Repeat(Int(0, 1, 2), num_pe_io_out)),
                flag_initial(Int(0, 1, 2))
            ).Else(
                en_r(Int(0, 1, 2)),
                en_counters(Repeat(Int(0, 1, 2), num_pe_io_out)),
                en_pop_r(Repeat(Int(0, 1, 2), num_pe_io_in)),
                en_push_r(Repeat(Int(0, 1, 2), num_pe_io_out)),
                done_r(Int(0, 1, 2)),
                Case(fsm_state)(
                    When(FSM_IDLE)(
                        If(start)(
                            fsm_state(FSM_PROCESS)
                        )
                    ),
                    When(FSM_PROCESS)(
                        If(Land(Uand(available_push_masked), Uand(available_pop_masked)))(
                            en_r(Int(1, 1, 2)),
                            en_counters(Repeat(Int(1, 1, 2), num_pe_io_out)),
                            en_pop_r(Repeat(Int(1, 1, 2), num_pe_io_in)),
                            en_push_r(Repeat(Int(1, 1, 2), num_pe_io_in)),
                            flag_initial(Int(1, 1, 2))
                        ).Elif(Uand(write_fifo_done_masked))(
                            fsm_state(FSM_DONE),
                            done_r(Int(1, 1, 2))
                        ).Elif(AndList(Uand(available_push_masked), flag_initial, Uand(read_fifo_done_masked)))(
                            en_r(Int(1, 1, 2)),
                            en_push_r(Repeat(Int(1, 1, 2), num_pe_io_out)),
                            en_counters(Repeat(Int(1, 1, 2), num_pe_io_out))
                        )
                    ),
                    When(FSM_DONE)(
                        If(~start)(
                            fsm_state(FSM_IDLE)
                        )
                    )
                )
            )
        )
        j = m.Genvar('j')
        genfor = m.GenerateFor(j(0), j < num_pe_io_out, j.inc(), 'genfor_ignore')
        igc = self.create_ignore_counter()
        params = [('width', 16)]
        con = [('clk', clk), ('rst', rst), ('start', en_counters[j]),
               ('limit', write_fifo_ignore[j * 16:(j + 1) * 16]),
               ('loop_limit', write_fifo_loop_ignore[j * 16:(j + 1) * 16]), ('out', ignore_counter_out[j])]

        genfor.Instance(igc, 'ignore_counter', params, con)

        initialize_regs(m, {'fsm_state': FSM_IDLE})

        self.cache[name] = m
        return m

    def create_fecth_data(self):
        name = 'fecth_data'
        if name in self.cache.keys():
            return self.cache[name]
        m = Module(name)
        INPUT_DATA_WIDTH = m.Parameter('INPUT_DATA_WIDTH', 512)
        OUTPUT_DATA_WIDTH = m.Parameter('OUTPUT_DATA_WIDTH', 16)

        clk = m.Input('clk')
        start = m.Input('start')
        rst = m.Input('rst')

        request_read = m.OutputReg('request_read')
        data_valid = m.Input('data_valid')
        read_data = m.Input('read_data', INPUT_DATA_WIDTH)

        pop_data = m.Input('pop_data')
        available_pop = m.OutputReg('available_pop')
        data_out = m.Output('data_out', OUTPUT_DATA_WIDTH)

        NUM = m.Localparam('NUM', INPUT_DATA_WIDTH / OUTPUT_DATA_WIDTH)

        fsm_read = m.Reg('fsm_read', 2)
        fsm_control = m.Reg('fsm_control', 2)
        data = m.Reg('data', INPUT_DATA_WIDTH)
        buffer = m.Reg('buffer', INPUT_DATA_WIDTH)
        count = m.Reg('count', NUM)
        has_buffer = m.Reg('has_buffer')
        buffer_read = m.Reg('buffer_read')
        en = m.Reg('en')

        m.EmbeddedCode('')
        data_out.assign(data[0:OUTPUT_DATA_WIDTH])

        m.Always(Posedge(clk))(
            If(rst)(
                en(Int(0, 1, 2))
            ).Else(
                en(Mux(en, en, start))
            )
        )

        m.Always(Posedge(clk))(
            If(rst)(
                fsm_read(0),
                request_read(0),
                has_buffer(0)
            ).Else(
                request_read(0),
                Case(fsm_read)(
                    When(0)(
                        If(en & data_valid)(
                            buffer(read_data),
                            request_read(1),
                            has_buffer(1),
                            fsm_read(1)
                        )
                    ),
                    When(1)(
                        If(buffer_read)(
                            has_buffer(0),
                            fsm_read(0)
                        )
                    )
                )
            )
        )

        m.Always(Posedge(clk))(
            If(rst)(
                fsm_control(0),
                available_pop(0),
                count(0),
                buffer_read(0)
            ).Else(
                buffer_read(0),
                Case(fsm_control)(
                    When(0)(
                        If(has_buffer)(
                            data(buffer),
                            count(1),
                            buffer_read(1),
                            available_pop(1),
                            fsm_control(1)
                        )
                    ),
                    When(1)(
                        If(pop_data & ~count[NUM - 1])(
                            count(count << 1),
                            data(data[OUTPUT_DATA_WIDTH:512])
                        ),
                        If(pop_data & count[NUM - 1] & has_buffer)(
                            count(1),
                            data(buffer),
                            buffer_read(1)
                        ),
                        If(count[NUM - 1] & pop_data & ~has_buffer)(
                            count(count << 1),
                            data(data[OUTPUT_DATA_WIDTH:512]),
                            available_pop(0),
                            fsm_control(0)
                        )
                    )
                )
            )
        )

        initialize_regs(m)

        self.cache[name] = m
        return m

    def create_dispath_data(self):
        name = 'dispath_data'
        if name in self.cache.keys():
            return self.cache[name]

        m = Module(name)
        INPUT_DATA_WIDTH = m.Parameter('INPUT_DATA_WIDTH', 16)
        OUTPUT_DATA_WIDTH = m.Parameter('OUTPUT_DATA_WIDTH', 512)

        clk = m.Input('clk')
        rst = m.Input('rst')

        available_write = m.Input('available_write')
        request_write = m.OutputReg('request_write')
        write_data = m.OutputReg('write_data', OUTPUT_DATA_WIDTH)

        push_data = m.Input('push_data')
        available_push = m.OutputReg('available_push')
        data_in = m.Input('data_in', INPUT_DATA_WIDTH)

        NUM = m.Localparam('NUM', OUTPUT_DATA_WIDTH / INPUT_DATA_WIDTH)
        m.EmbeddedCode('')
        fsm_control = m.Reg('fsm_control', 2)
        buffer1 = m.Reg('buffer1', OUTPUT_DATA_WIDTH)
        buffer2 = m.Reg('buffer2', OUTPUT_DATA_WIDTH)
        count1 = m.Reg('count1', NUM)
        count2 = m.Reg('count2', NUM)
        request_write1 = m.Reg('request_write1')
        request_write2 = m.Reg('request_write2')
        request_write11 = m.Reg('request_write11')
        request_write22 = m.Reg('request_write22')

        m.Always(Posedge(clk))(
            If(rst)(
                request_write(0),
                request_write11(0),
                request_write22(0)
            ).Else(
                request_write11(request_write1),
                request_write22(request_write2),
                request_write(request_write11 | request_write22),
                If(request_write11)(
                    write_data(buffer1)
                ).Elif(request_write22)(
                    write_data(buffer2)
                )
            )
        )
        m.Always(Posedge(clk))(
            If(rst)(
                available_push(1),
                fsm_control(0),
                count1(1),
                count2(1),
                request_write1(0),
                request_write2(0),
            ).Else(
                request_write1(0),
                request_write2(0),

                Case(fsm_control)(
                    When(0)(
                        If(push_data)(
                            buffer1(Or(Cat(data_in, Repeat(Int(0, 1, 2), OUTPUT_DATA_WIDTH - INPUT_DATA_WIDTH)),
                                       buffer1 >> INPUT_DATA_WIDTH)),
                            count1(count1 << 1)
                        ),
                        If(count1[NUM - 1] & push_data)(
                            fsm_control(1)
                        )
                    ),
                    When(1)(
                        If(available_write)(
                            count1(1),
                            request_write1(1),
                            available_push(1)
                        ),
                        If(available_write & available_push)(
                            fsm_control(2)
                        ),
                        If(available_write & ~available_push)(
                            fsm_control(3)
                        ),
                        If(push_data)(
                            buffer2(Or(Cat(data_in, Repeat(Int(0, 1, 2), OUTPUT_DATA_WIDTH - INPUT_DATA_WIDTH)),
                                       buffer2 >> INPUT_DATA_WIDTH)),
                            count2(count2 << 1)
                        ),
                        If(count2[NUM - 2] & push_data & ~available_write)(
                            available_push(0)
                        )
                    ),
                    When(2)(
                        If(push_data)(
                            buffer2(Or(Cat(data_in, Repeat(Int(0, 1, 2), OUTPUT_DATA_WIDTH - INPUT_DATA_WIDTH)),
                                       buffer2 >> INPUT_DATA_WIDTH)),
                            count2(count2 << 1)
                        ),
                        If(count2[NUM - 1] & push_data)(
                            fsm_control(3)
                        )
                    ),
                    When(3)(
                        If(available_write)(
                            request_write2(1),
                            available_push(1),
                            count2(1)
                        ),
                        If(available_write & available_push)(
                            fsm_control(0)
                        ),
                        If(available_write & ~available_push)(
                            fsm_control(1)
                        ),
                        If(push_data)(
                            buffer1(Or(Cat(data_in, Repeat(Int(0, 1, 2), OUTPUT_DATA_WIDTH - INPUT_DATA_WIDTH)),
                                       buffer1 >> INPUT_DATA_WIDTH)),
                            count1(count1 << 1)
                        ),
                        If(count1[NUM - 2] & push_data & ~available_write)(
                            available_push(0)
                        )
                    )
                )
            )
        )
        initialize_regs(m)
        self.cache[name] = m
        return m

    def create_ignore_counter(self):
        name = 'ignore_counter'
        if name in self.cache.keys():
            return self.cache[name]
        m = Module(name)
        width = m.Parameter('width', 32)

        clk = m.Input('clk')
        rst = m.Input('rst')
        start = m.Input('start')
        limit = m.Input('limit', width)
        loop_limit = m.Input('loop_limit', width)
        out = m.OutputReg('out')

        count = m.Reg('count', width)
        fsm = m.Reg('fsm')

        m.Always(Posedge(clk))(
            If(rst)(
                count(1),
                out(0),
                fsm(0)
            ).Else(
                out(0),
                If(start)(
                    Case(fsm)(
                        When(0)(
                            If(count == limit)(
                                out(1),
                                count(1),
                                fsm(1)
                            ).Else(
                                count.inc()
                            )
                        ),
                        When(1)(
                            If(count == loop_limit)(
                                out(1),
                                count(1)
                            ).Else(
                                count.inc()
                            )
                        )
                    )
                )
            )
        )
        initialize_regs(m)
        self.cache[name] = m
        return m

    def create_data_producer(self):
        name = 'data_producer'
        if name in self.cache.keys():
            return self.cache[name]
        m = Module(name)
        file = m.Parameter('file', 'file.txt')
        data_width = m.Parameter('data_width', 512)
        num_data = m.Parameter('num_data', 16)
        addr_width = m.Parameter('addr_width', 4)

        # Control signals for the component
        clk = m.Input('clk')
        rst = m.Input('rst')

        # Ports for delivery of data to the consumer
        request_read = m.Input('rd_request')
        read_data_valid = m.OutputReg('read_data_valid')
        read_done = m.OutputReg('rd_done')
        read_data = m.Output('read_data', data_width)

        re = m.Reg('re')
        data_counter = m.Reg('data_counter', addr_width)

        m.EmbeddedCode("\n")

        fsm_produce_data = m.Reg('fsm_produce_data', 2)
        fsm_init = m.Localparam('fsm_init', Int(0, fsm_produce_data.width, 10))
        fsm_produce = m.Localparam('fsm_produce',
                                   Int(1, fsm_produce_data.width, 10))
        fsm_done = m.Localparam('fsm_done', Int(2, fsm_produce_data.width, 10))

        m.EmbeddedCode("\n")

        m.Always(Posedge(clk))(
            If(rst)(
                data_counter(0),
                read_data_valid(Int(0, 1, 10)),
                read_done(Int(0, 1, 10)),
                re(Int(0, 1, 10)),
                fsm_produce_data(fsm_init),
            ).Else(
                Case(fsm_produce_data)(
                    When(fsm_init)(
                        re(Int(1, 1, 10)),
                        fsm_produce_data(fsm_produce)
                    ),
                    When(fsm_produce)(
                        re(Int(0, 1, 10)),
                        read_data_valid(Int(1, 1, 10)),
                        If(request_read)(
                            re(Int(1, 1, 10)),
                            data_counter(data_counter + 1),
                            read_data_valid(Int(0, 1, 10)),
                        ),
                        If(data_counter == num_data)(
                            read_data_valid(Int(0, 1, 10)),
                            fsm_produce_data(fsm_done)
                        )
                    ),
                    When(fsm_done)(
                        read_done(Int(1, 1, 10))
                    ),
                )
            )
        )
        params = [('init_file', file), ('data_width', data_width),
                  ('addr_width', addr_width)]
        con = [('clk', clk),
               ('we', Int(0, 1, 2)),
               ('re', re),
               ('raddr', data_counter),
               ('waddr', data_counter),
               ('din', Repeat(Int(0, 1, 2), data_width)),
               ('dout', read_data)]
        mem = Components().create_memory()
        m.Instance(mem, 'mem_rom', params, con)

        initialize_regs(m)
        self.cache[name] = m

        return m

    def create_data_consumer(self):
        name = 'data_consumer'
        if name in self.cache.keys():
            return self.cache[name]
        m = Module(name)
        id = m.Parameter('id', 0)
        data_width = m.Parameter('data_width', 512)
        num_data = m.Parameter('num_data', 16)
        counter_num_data_width = m.Parameter('counter_num_data_width', 4)

        # Control signals for the component
        clk = m.Input('clk')
        rst = m.Input('rst')

        # comunication buses for the cgra output data
        wr_available = m.OutputReg('wr_available')
        wr_request = m.Input('wr_request')
        wr_data = m.Input('wr_data', data_width)
        wr_done = m.OutputReg('wr_done')

        counter = m.Reg('counter', counter_num_data_width)

        m.Always(Posedge(clk))(
            If(rst)(
                counter(0),
                wr_done(Int(0, 1, 10)),
                wr_available(Int(0, wr_available.width, 10)),
            ).Else(
                wr_available(Int(1, wr_available.width, 10)),
                If(And(wr_request, Not(wr_done)))(
                    Display("%d:%h", id, wr_data),
                    counter(counter + 1),
                ),
                If(counter == num_data)(
                    wr_done(Int(1, 1, 10)),
                    wr_available(Int(0, wr_available.width, 10)),
                )
            )
        )

        initialize_regs(m)
        self.cache[name] = m

        return m

    def create_acc_reset(self):
        name = 'acc_reset'
        if name in self.cache.keys():
            return self.cache[name]

        m = Module(name)
        width = m.Parameter('width', 32)

        clk = m.Input('clk')
        rst = m.Input('rst')
        start = m.Input('start')
        limit = m.Input('limit', width)
        out = m.OutputReg('out')

        count = m.Reg('count', width)

        m.Always(Posedge(clk))(
            If(rst)(
                count(1),
                out(0)
            ).Else(
                out(0),
                If(start)(
                    If(count == limit)(
                        out(1),
                        count(1),
                    ).Else(
                        count.inc()
                    )
                )
            )
        )
        initialize_regs(m)
        self.cache[name] = m
        return m
