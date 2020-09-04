import argparse
from veriloggen import *
from cgra import Cgra
from create_top_level_module import create_top_level_synth, create_top_level_sim
from utils import commands_getoutput, split_modules


def write_file(name, string):
    with open(name, 'w') as fp:
        fp.write(string)
        fp.close()


def create_args():
    parser = argparse.ArgumentParser('create_project -h')

    parser.add_argument('-v', '--verilog', help='Verilog file of CGRA', type=str)
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

    if args.verilog:
        args.verilog = running_path + '/' + args.verilog
        m = from_verilog.read_verilog_module(args.verilog)['cgra']
        msynth = create_top_level_synth(m)
        msim = create_top_level_sim(m)

    elif args.json:
        args.json = running_path + '/' + args.json
        m = Cgra()
        m.load_from_file(args.json)
        m = m.get()
        msynth = create_top_level_synth(m)
        msim = create_top_level_sim(m)

    else:
        raise Exception('Missing parameters. Run create_project -h to see all parameters needed')

    modules1 = split_modules(msynth.to_verilog())
    modules2 = split_modules(msim.to_verilog())
    msynth = modules1['top_level_synth']
    msim = modules2['top_level_sim']
    commands_getoutput('cp -r %s/resources/template.prj %s/%s' % (hpcgra_root, args.output, args.name))
    m.to_verilog('%s/%s/src/%s.v' % (args.output, args.name, m.name))
    write_file('%s/%s/src/top_level_synth.v' % (args.output, args.name), msynth)
    write_file('%s/%s/src/top_level_sim.v' % (args.output, args.name), msim)
    commands_getoutput(
        'rm -rf %s/src/parser.out %s/src/parsetab.py %s/src/__pycache__' % (hpcgra_root, hpcgra_root, hpcgra_root))
    print('Project successfully created in %s/%s' % (args.output, args.name))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
