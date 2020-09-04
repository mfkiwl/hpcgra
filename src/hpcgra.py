import argparse
from cgra import Cgra
from cgra_architectures import create_cgra
from cgra_assembly import CgraAssembly


def create_args():
    parser = argparse.ArgumentParser('hpcgra -h')
    parser.add_argument('--arch', help='CGRA architecture.', type=str,
                        choices=['mesh', 'one-hop', 'chess', 'hexagonal', 'diagonal'])
    parser.add_argument('-s', '--shape',
                        help='CGRA architecture shape NxM, where N is number of columns and M number of rows.')
    parser.add_argument('--isa', help='List of CGRA architecture instruction set.')
    parser.add_argument('--fifos', help='Size of PE balancing fifos.', default=0, type=int)
    parser.add_argument('--routes', default=0, type=int,
                        help='Number of inputs and to be routed to outputs,\
                         0 only the output of the ALU is sent to outputs.')
    parser.add_argument('--acc', help='This flag adding an accumulator to all PE.', action="store_true")
    parser.add_argument('--data_width', help='CGRA data width.', type=int, default=8)
    parser.add_argument('--conf_bus_width', help='CGRA configuration bus data width.', type=int, default=8)
    parser.add_argument('-a', '--assembly', help='Assembly input file.', type=str)
    parser.add_argument('-c', '--compile', help='Compile assembly file to CGRA bitstream.', action="store_true")
    parser.add_argument('-j', '--json', help='Architecture JSON description file.', type=str)
    parser.add_argument('-b', '--bitstream', help='Bitstream output file.', type=str)
    parser.add_argument('-v', '--verilog', help='Verilog output file.', type=str)

    args = parser.parse_args()

    return args


def main():
    args = create_args()
    cgra = Cgra()
    if args.json or args.arch:
        if args.json:
            cgra.load_from_file(args.json)
        else:
            if args.shape:
                v = args.shape.split('x')
                n, m = int(v[0]), int(v[1])
                if args.isa:
                    isa = args.isa.split(',')
                    json_str = create_cgra(args.arch, (n, m), isa, args.routes, args.fifos, args.acc, args.data_width,
                                           args.conf_bus_width)
                    cgra.load_from_string(json_str)
                else:
                    raise Exception('Missing isa parameter.')
            else:
                raise Exception('Missing shape parameter.')
        if args.compile:
            if not args.assembly:
                Exception('Missing assembly file parameter.')
            elif not args.bitstream:
                Exception('Missing bitstream file parameter.')
            else:
                ca = CgraAssembly(cgra, args.assembly, args.bitstream)
                ca.compile()

        if args.verilog:
            cgra.get().to_verilog(args.verilog)
            print('Verilog code generates with success, file save in %s' % args.verilog)

    else:
        raise Exception("Architecture JSON file not found. Run hpcgra -h to see all parameters needed")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
