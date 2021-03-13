# TODO DESCRIPTION AND COMMENTS
from src.hw.bitstream import Bitstream
from src.hw.cgra import Cgra
from src.hw.cgra_accelerator import CgraAccelerator
from src.hw.create_testbench_module import create_testbench_sim
from src.simul.util.os_util_functions import correct_directory_path, search_a_path, save_file


class VerilogSimulator:

    def __init__(self, files, paths: str):
        self._files = files
        self._paths = paths
        # creating the initial config file for the CGRA simulation
        self._initial_conf = Bitstream(self.search_json_file(),
                                       self.search_asm_file()).get()
        # creating the CGRA HW
        self._cgra = Cgra(self.search_json_file())
        # creating the cgra accelarator top
        self._cgra_acc = CgraAccelerator(self._cgra)
        # create the HW verilog file
        cgra_acc_testbench_verilog = \
            create_testbench_sim(self._cgra_acc).to_verilog()
        method = "w"
        file = correct_directory_path(
            search_a_path("verilog_simul/verilog_src", paths)) + "test_bench.v"
        save_file(file, cgra_acc_testbench_verilog, method)

    # TODO
    def start(self):
        pass

    def search_json_file(self):
        for file in self._files:
            if ".json" in file:
                return file
        raise Exception("Error! No .json file found.")

    def search_asm_file(self):
        for file in self._files:
            if ".asm" in file:
                return file
        raise Exception("Error! No .asm file found.")
