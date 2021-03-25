import argparse
import os
import sys
import traceback

p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if not p in sys.path:
    sys.path.insert(0, p)

from src.hw.cgra_bitstream import Bitstream


def create_args():
    parser = argparse.ArgumentParser('generate_bitstream -h')
    parser.add_argument('-j', '--json', help='CGRA architecture description JSON file', type=str)
    parser.add_argument('-a', '--assembly', help='Assembly code', type=str)
    parser.add_argument('-o', '--output', help='Bitstream File', type=str, default='a.bit')

    return parser.parse_args()


def main():
    args = create_args()
    running_path = os.getcwd()
    os.chdir(os.path.dirname(__file__))

    if args.json and args.assembly:
        args.json = running_path + '/' + args.json
        args.assembly = running_path + '/' + args.assembly
        bitstream = Bitstream(args.json, args.assembly)
        bitstream.save(running_path + '/' + args.output)
    else:

        raise Exception('Missing parameters. Run generate_bitstream -h to see all parameters needed')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('Exception in:', exc_type, fname, exc_tb.tb_lineno)
        traceback.print_exc()
