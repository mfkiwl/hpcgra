import argparse
import traceback

from veriloggen import *

from cgra import Cgra
from cgra_accelerator import CgraAccelerator
from create_acc_axi_interface import AccAXIInterface
from create_testbench_module import create_testbench_sim, create_testbench_synth
from utils import commands_getoutput, split_modules


def write_file(name, string):
    with open(name, 'w') as fp:
        fp.write(string)
        fp.close()


def create_args():
    parser = argparse.ArgumentParser('create_project -h')
    parser.add_argument('-j', '--json', help='CGRA architecture description JSON file', type=str)
    parser.add_argument('-n', '--name', help='Project name', type=str, default='a.prj')
    parser.add_argument('-o', '--output', help='Project location', type=str, default='.')

    return parser.parse_args()


def main():
    args = create_args()
    running_path = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    hpcgra_root = os.getcwd() + '/../'

    if args.output == '.':
        args.output = running_path

    if args.json:
        args.json = running_path + '/' + args.json
        cgra = Cgra(args.json)
        cgraacc = CgraAccelerator(cgra)
        acc_axi = AccAXIInterface(cgraacc).create_kernel_top()
        msynth = create_testbench_synth(cgraacc)
        msim = create_testbench_sim(cgraacc)
        cgraacc_code = cgraacc.get()

        modules1 = split_modules(msynth.to_verilog())
        modules2 = split_modules(msim.to_verilog())
        modules3 = split_modules(acc_axi.to_verilog())

        msynth = modules1['testbench_synth']

        msim = modules2['testbench_sim'] + '\n\n' + modules2['mem_rom_control'] + '\n\n' + modules2['memory']

        maxi = modules3['kernel_top'] + '\n\n' + \
               modules3['app_top'] + '\n\n' + \
               modules3['control_s_axi_%d' % cgraacc.get_num_in()] + '\n\n' + \
               modules3['axi_reader'] + '\n\n' + \
               modules3['axi_writer'] + '\n\n' + \
               modules3['axi_counter'] + '\n\n' + \
               modules3['xpm_fifo_sync_wrapper']

        commands_getoutput('cp -r %s/resources/template.prj %s/%s' % (hpcgra_root, args.output, args.name))

        cgraacc_code.to_verilog('%s/%s/src/%s.v' % (args.output, args.name, cgraacc_code.name))

        write_file('%s/%s/src/testbench_synth.v' % (args.output, args.name), msynth)
        write_file('%s/%s/src/testbench_sim.v' % (args.output, args.name), msim)
        write_file('%s/%s/src/kernel_top.v' % (args.output, args.name), maxi)
        write_file('%s/%s/synth/xilinx/num_m_axis.mk' % (args.output, args.name),
                   'NUM_M_AXIS=%d' % cgraacc.get_num_in())

        commands_getoutput(
            'rm -rf %s/src/parser.out %s/src/parsetab.py %s/src/__pycache__' % (hpcgra_root, hpcgra_root, hpcgra_root))

        print('Project successfully created in %s/%s' % (args.output, args.name))
    else:
        raise Exception('Missing parameters. Run create_project -h to see all parameters needed')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
        traceback.print_exc()
