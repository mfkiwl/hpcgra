# Main simulator archive
# TODO DESCRIPTION AND COMMENTS

from simul_verilog.simulation.verilog_simulator import VerilogSimulator
from util.simul_util_functions import init_folders, search_for_files, correct_directory_path

from src.simul.simul_dot.simulation.dot_simulator import DotSimulator


class MainSimul:

    def __init__(self, test_path: str, type_of_input_generation: int,
                 tam_input_data: int):
        self._test_path = correct_directory_path(test_path)
        self._type_of_input_generation = type_of_input_generation
        self._tam_input_data = tam_input_data
        self._paths = [test_path + "verilog_simul", test_path + "dot_simul",
                       test_path + "verilog_simul/input_files",
                       test_path + "verilog_simul/output_files",
                       test_path + "dot_simul/output_files",
                       test_path + "verilog_simul/verilog_src"]
        init_folders(self._paths)
        self._files = search_for_files(self._test_path)

    def start_dot_simul(self):
        dotsimulator = DotSimulator(self._files)
        dotsimulator.start(self._type_of_input_generation,
                           self._tam_input_data,
                           self._paths)

    def start_verilog_simul(self):
        verilogsimulator = VerilogSimulator(self._files)
        verilogsimulator.start(self._type_of_input_generation,
                               self._tam_input_data,
                               self._paths)

    def start_both_simul(self):
        self.start_dot_simul()
        self.start_verilog_simul()


if __name__ == "__main__":
    test_path = "/home/jeronimo/Documentos/GIT/hpcgra/simul_tests/test1/"
    type_of_input_generation = 1
    tam_input_data = 33

    simul = MainSimul(test_path, type_of_input_generation, tam_input_data)
    simul.start_both_simul()
