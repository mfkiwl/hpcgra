import argparse
import os
import sys
import traceback

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not p in sys.path:
    sys.path.insert(0, p)

from veriloggen import *

from src.hw.cgra import Cgra
from src.hw.cgra_accelerator import CgraAccelerator
from src.hw.create_acc_axi_interface import AccAXIInterface
from src.hw.utils import commands_getoutput


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
        acc_axi = AccAXIInterface(cgraacc)

        commands_getoutput('cp -r %s/resources/template.prj %s/%s' % (hpcgra_root, args.output, args.name))

        acc_axi.create_kernel_top(args.name).to_verilog(
            '%s/%s/xilinx_aws_f1/hw/src/%s.v' % (args.output, args.name, args.name))

        write_file('%s/%s/xilinx_aws_f1/hw/simulate/num_m_axis.mk' % (args.output, args.name),
                   'NUM_M_AXIS=%d' % cgraacc.get_num_in())

        write_file('%s/%s/xilinx_aws_f1/hw/synthesis/num_m_axis.mk' % (args.output, args.name),
                   'NUM_M_AXIS=%d' % cgraacc.get_num_in())

        write_file('%s/%s/xilinx_aws_f1/sw/host/prj_name' % (args.output, args.name), args.name)

        write_file('%s/%s/xilinx_aws_f1/hw/simulate/prj_name' % (args.output, args.name), args.name)

        write_file('%s/%s/xilinx_aws_f1/hw/synthesis/prj_name' % (args.output, args.name), args.name)

        write_file('%s/%s/xilinx_aws_f1/hw/simulate/vitis_config.txt' % (args.output, args.name),
                   acc_axi.get_connectivity_config(args.name))

        write_file('%s/%s/xilinx_aws_f1/hw/synthesis/vitis_config.txt' % (args.output, args.name),
                   acc_axi.get_connectivity_config(args.name))

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
