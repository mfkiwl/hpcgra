from veriloggen import *

from components import Components
from utils import initialize_regs

def create_top_level_synth(module):
    m = Module('top_level_synth')
    clk = m.Input('clk')
    rst = m.Input('rst')
    out = m.Output('out')
    regs_reset = []
    regs_inc = []
    orlist = ''

    params = module.get_params()
    for p in params:
        m.Localparam(params[p].name, params[p].value)

    ports = module.get_ports()
    con = []
    max_width_out = 1
    for port in ports:
        if module.is_input(port) and port in ['clk', 'rst']:
            con.append((port, m.get_ports()[port]))
        elif module.is_input(port) and port not in ['clk', 'rst']:
            p = ports[port]
            if p.width:
                reg = m.Reg(port, p.width)
            else:
                reg = m.Reg(port)
            regs_reset.append(reg(0))
            regs_inc.append(reg.inc())
            con.append((port, reg))
        elif module.is_output(port):
            p = ports[port]
            if p.width:
                if str(p.width) in params:
                    p.width = p.width.value

                wire = m.Wire(module.name + '_' + port, p.width)
                max_width_out = max(max_width_out, p.width)
            else:
                wire = m.Wire(module.name + '_' + port)
            orlist += wire.name + '|'
            con.append((port, wire))

    data = m.Wire('data', max_width_out)

    m.Instance(module, module.name, params, con)

    m.Always(Posedge(clk))(
        If(rst)(
            regs_reset
        ).Else(
            regs_inc
        )
    )

    data.assign(EmbeddedCode(orlist[:-1]))
    out.assign(Uxor(data))

    initialize_regs(m)

    return m


def create_top_level_sim(module, assignment_rule=None, reset_values=None, max_sim_time=1000000, clock=5,
                         parameters=None):
    if assignment_rule is None:
        assignment_rule = {}

    if reset_values is None:
        reset_values = {}

    if parameters is None:
        parameters = {'init_file': 'mem_file.txt'}

    mem_size_bits = 20
    m = Module('top_level_sim')
    params = []
    mparams = module.get_params()
    for p in mparams:
        if p in parameters.keys():
            params.append((p, m.Localparam(p, parameters[p])))
        else:
            params.append((p, m.Localparam(p, mparams[p].value)))

    ports = module.get_ports()
    if 'clk' not in ports:
        clk = m.Reg('clk')
    else:
        clk = ports['clk']

    if 'rst' not in ports:
        rst = m.Reg('rst')
    else:
        rst = ports['rst']

    regs_reset = []
    regs_assignment = []
    orlist = ''

    con = []
    for port in ports:
        if module.is_input(port):
            p = ports[port]
            if p.width:
                reg = m.Reg(port, p.width)
            else:
                reg = m.Reg(port)
            if port != 'clk' and port != 'rst' and port != 'conf_bus':
                if port in assignment_rule.keys():
                    regs_assignment.append(reg(assignment_rule[port]))
                else:
                    regs_assignment.append(reg.inc())

                if port in reset_values.keys():
                    regs_reset.append(reg(reset_values[port]))
                else:
                    regs_reset.append(reg(0))

            con.append((port, reg))

        elif module.is_output(port) and port not in m.get_ports():
            p = ports[port]
            if p.width:
                wire = m.Wire(port, p.width)
            else:
                wire = m.Wire(port)
            orlist += wire.name + '|'
            con.append((port, wire))

    mem_conf_re = m.Reg('mem_conf_re')
    mem_conf_we = m.Reg('mem_conf_we')
    mem_conf_addr = m.Reg('mem_conf_addr', mem_size_bits)
    mem_conf_din = m.Reg('mem_conf_din', ports['conf_bus'].width)
    mem_conf_dout = m.Wire('mem_conf_dout', ports['conf_bus'].width)
    memory = Components().create_memory()
    mmparams = [('init_file', parameters['init_file']), ('data_width', ports['conf_bus'].width),
                ('addr_width', mem_size_bits)]
    mmcon = [('clk', clk), ('we', mem_conf_we), ('re', mem_conf_re), ('raddr', mem_conf_addr), ('waddr', mem_conf_addr),
             ('din', mem_conf_din), ('dout', mem_conf_dout)]
    m.Instance(memory, 'mem_conf', mmparams, mmcon)

    m.Instance(module, module.name, params, con)

    regs_reset.append(mem_conf_re(0))
    regs_reset.append(mem_conf_we(0))
    regs_reset.append(mem_conf_addr(0))
    regs_reset.append(mem_conf_din(0))

    initialize_regs(m, {'clk': 0, 'rst': 1})

    m.Initial(
        EmbeddedCode('@(posedge clk);'),
        EmbeddedCode('@(posedge clk);'),
        EmbeddedCode('@(posedge clk);'),
        rst(0),
        EmbeddedCode('#%d$finish();' % max_sim_time)
    )
    m.EmbeddedCode('always #%dclk=~clk;' % clock)

    m.Always(Posedge(clk))(
        If(rst)(
            regs_reset
        ).Else(
            mem_conf_re(0),
            ports['conf_bus'](0),
            If(mem_conf_addr < Power(2, 10) - 1)(
                mem_conf_re(1),
                If(mem_conf_re)(
                    mem_conf_addr.inc(),
                    ports['conf_bus'](mem_conf_dout)
                )
            ).Else(
                regs_assignment
            )
        )
    )

    return m
