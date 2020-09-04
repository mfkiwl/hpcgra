from cgra import Cgra
from cgra_assembly import CgraAssembly
from cgra_configuration import CgraConfiguration
from create_top_level_module import create_top_level_sim, create_top_level_synth


def test_gen_synth():
    toplevel_file = '../test/cgra_16x16.prj/src/top_synth_cgra.v'
    cgra = Cgra('../test/cgra_mesh_2x2.json')
    create_top_level_synth(cgra.get()).to_verilog(toplevel_file)


def test_assembly():
    bitstream_file = '/media/lucas/3CF6B349F6B301E6/UFV/Projetos/Projetos-Pos-Graduacao/Doutorado/hpcgra/test/sum.bit'
    toplevel_file = '../test/cgra_16x16.prj/src/top_sim_cgra.v'
    params = {'init_file': bitstream_file}
    cgra = Cgra('../test/cgra_mesh_2x2.json')
    create_top_level_sim(cgra.get(), parameters=params).to_verilog(toplevel_file)
    ca = CgraAssembly(cgra, '../test/sum.asm')
    ca.compile()


def test_router_conf():
    cgra = Cgra('../test/cgra_mesh_2x2.json')
    create_top_level_sim(cgra.get()).to_verilog('../test/cgra_16x16.prj/src/top_sim_cgra.v')
    cc = CgraConfiguration(cgra)
    f = open('../test/cgra_16x16.prj/sim/vcsmx/mem_file.txt', 'w')
    conf = cc.create_reset_conf(0)
    conf += cc.create_router_conf(3, {'alu': 'stream'})
    for c in conf:
        f.write(c)
        f.write('\n')
        print(c)
    f.close()


def test_alu_conf():
    cgra = Cgra('../test/cgra_mesh_2x2.json')
    create_top_level_sim(cgra.get()).to_verilog('../test/cgra_16x16.prj/src/top_sim_cgra.v')
    cc = CgraConfiguration(cgra)
    f = open('../test/cgra_16x16.prj/sim/vcsmx/mem_file.txt', 'w')
    conf = cc.create_reset_conf(0)
    conf += cc.create_alu_conf(0, 'add', ['istream', 'const'], [0, 0])
    conf += cc.create_alu_conf(0, 'sub', [1, 2], [0, 0])
    for c in conf:
        f.write(c)
        f.write('\n')
        print(c)
    f.close()


def test_alu_delay_conf():
    cgra = Cgra('../test/cgra_mesh_2x2.json')
    create_top_level_sim(cgra.get()).to_verilog('../test/cgra_16x16.prj/src/top_sim_cgra.v')
    cc = CgraConfiguration(cgra)
    f = open('../test/cgra_16x16.prj/sim/vcsmx/mem_file.txt', 'w')
    conf = cc.create_reset_conf(0)
    conf += cc.create_alu_conf(0, 'add', ['load', 'const'], [0, 0])
    conf += cc.create_alu_conf(0, 'sub', [1, 2], [0, 0])
    for c in conf:
        f.write(c)
        f.write('\n')
        print(c)
    f.close()


def test_const_conf():
    cgra = Cgra('../test/cgra_mesh_2x2.json')
    create_top_level_sim(cgra.get()).to_verilog('../test/cgra_16x16.prj/src/top_sim_cgra.v')
    cc = CgraConfiguration(cgra)
    f = open('../test/cgra_16x16.prj/sim/vcsmx/mem_file.txt', 'w')
    conf = cc.create_reset_conf(0)
    for i in range(256):
        conf += cc.create_const_conf(0, i)
    for c in conf:
        f.write(c)
        f.write('\n')
        print(c)
    f.close()


# test_const_conf()
# test_alu_conf()
# test_alu_delay_conf()
# test_router_conf()
# test_assembly()
# test_gen_synth()
