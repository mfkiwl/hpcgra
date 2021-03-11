# Main simulator archive
# TODO DESCRIPTION AND COMMENTS
from simul_dot.simulation.dot_simulator import DotSimulator
from simul_verilog.simulation.verilog_simulator import VerilogSimulator
from util.os_util_functions import init_folders, search_for_files


class Simul:

    def __init__(self, test_path: str, type_of_input_generation: int,
                 tam_input_data: int):
        self._test_path = test_path
        self._type_of_input_generation = type_of_input_generation
        self._tam_input_data = tam_input_data
        self._paths = [test_path + "verilog", test_path + "input_files",
                       test_path + "output_files_dot",
                       test_path + "output_files_verilog"]
        self._files = []

    def start(self):
        init_folders(self._paths)
        self._files = search_for_files(self._test_path)
        dotsimulator = DotSimulator(self._files)
        dotsimulator.start(self._type_of_input_generation,
                           self._tam_input_data, self._paths)
        verilogsimulator = VerilogSimulator(self._files)


if __name__ == "__main__":
    test_path = "/home/jeronimo/Documentos/GIT/hpcgra/simul_tests/test1/"
    cgra_gen = "/home/jeronimo/Documentos/GIT/hpcgra/src/cgra.py"
    bin_gen = "/home/jeronimo/Documentos/GIT/hpcgra/bin/generate_bitstream"
    type_of_input_generation = 1
    tam_input_data = 10
    '''
    if len(sys.argv) > 1:
        test_path = sys.argv[1]
        cgra_gen_path = sys.argv[2]
        bin_gen = sys.argv[3]
        type_of_input_generation = int(sys.argv[4])
        tam_input_data = int(sys.argv[5])
    else:
        print("Error!\n")
        print("Usage: <test_path> <cgra_gen_path> < = sys.argv[2]> 
        <type_of_input_generation> <tam_input_data>")
        exit(0)
    '''
    simul = Simul(test_path, type_of_input_generation, tam_input_data)
    simul.start()
