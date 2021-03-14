from veriloggen import *
from math import ceil, log2

from src.hw.components import Components
from src.hw.utils import initialize_regs


def create_data_producer(num_data):
    addr_width = ceil(log2(num_data))

    name = 'data_producer'
    # if name in self.cache.keys():
    #    return self.cache[name]
    m = Module(name)
    file = m.Parameter('file', 'file.txt')
    data_width = m.Parameter('data_width', 512)

    # Control signals for the component
    clk = m.Input('clk')
    rst = m.Input('rst')

    # Ports for delivery of data to the consumer
    request_read = m.Input('rd_request')
    read_data_valid = m.OutputReg('read_data_valid')
    read_done = m.OutputReg('rd_done')
    read_data = m.Output('read_data', data_width)

    re = m.Wire('re')

    m.EmbeddedCode("\n")

    re_fsw = m.Reg('re_fsw')
    data_counter = m.Reg('data_counter', addr_width)

    m.EmbeddedCode("\n")

    fsm_produce_data = m.Reg('fsm_produce_data', 2)
    fsm_init1 = m.Localparam('fsm_init1', Int(0, fsm_produce_data.width, 10))
    fsm_init2 = m.Localparam('fsm_init2', Int(1, fsm_produce_data.width, 10))
    fsm_produce = m.Localparam('fsm_produce', Int(2, fsm_produce_data.width, 10))
    fsm_done = m.Localparam('fsm_done', Int(3, fsm_produce_data.width, 10))

    m.EmbeddedCode("\n")

    re.assign(Or(re_fsw, request_read))

    m.Always(Posedge(clk))(
        If(rst)(
            data_counter(Int(0, data_counter.width, 10)),
            read_data_valid(Int(0, 1, 10)),
            read_done(Int(0, 1, 10)),
            fsm_produce_data(fsm_init1)
        ).Else(
            Case(fsm_produce_data)(
                When(fsm_init1)(
                    re_fsw(Int(1, 1, 10)),
                    fsm_produce_data(fsm_init2)
                ),
                When(fsm_init2)(
                    read_data_valid(Int(1, 1, 10)),
                    fsm_produce_data(fsm_produce)
                ),
                When(fsm_produce)(
                    read_data_valid(request_read),
                    If(request_read)(
                        data_counter(data_counter + Int(1, data_counter.width, 10))
                    ),
                    If(data_counter == Int(num_data-1,data_counter.width,10))(
                        fsm_produce_data(fsm_done)
                    )
                ),
                When(fsm_done)(
                    read_data_valid(Int(1,1,10)),
                    read_done(Int(1,1,10))
                ),
            )
        )
    )
    params = [('init_file', file), ('data_width', data_width), ('addr_width', addr_width)]
    con = [('clk', clk), ('we', Int(0, 1, 2)), ('re', re), ('raddr', data_counter),
           ('waddr', data_counter),
           ('din', Repeat(Int(0, 1, 2), data_width)),
           ('dout', read_data)]
    mem = Components().create_memory()
    m.Instance(mem, 'mem_rom', params, con)

    initialize_regs(m)
#   #     self.cache[name] = m

    return m


m = create_data_producer(10)
verilog = m.to_verilog("/home/jeronimo/Documentos/GIT/hpcgra/simul_tests/test1/verilog_simul/verilog_src/test_bench.v")
