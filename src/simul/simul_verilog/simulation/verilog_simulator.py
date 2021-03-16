# TODO DESCRIPTION AND COMMENTS
from src.hw.bitstream import Bitstream
from src.hw.cgra import Cgra
from src.hw.cgra_accelerator import CgraAccelerator
from src.hw.create_testbench_module import create_testbench_sim
from src.hw.utils import to_hex
from src.simul.util.queue import Queue
from src.simul.util.simul_util_functions import correct_directory_path, \
    search_a_path, save_file, generate_input_sequence


class VerilogSimulator:

    def __init__(self, files):
        self._files = files

    # TODO
    def start(self, type_of_input_generation: int, tam_input_data: int, paths):
        # creating the CGRA HW
        cgra = Cgra(self.search_json_file())
        # creating the cgra accelarator top
        cgra_acc = CgraAccelerator(cgra)
        # creating the initial config file for the CGRA simulation
        initial_conf = Bitstream(self.search_json_file(),
                                 self.search_asm_file()).get()
        input_files = []
        # creating the initial input files
        # TODO This code was made for 16b processing algorithms.
        # TODO It needs to be improved for other widths of data!!!
        for i in range(len(cgra_acc.cgra.input_ids)):
            # creating the input data
            data_in = generate_input_sequence(type_of_input_generation,
                                              tam_input_data)
            data_to_write = ""
            if i == 0:
                data_to_write = initial_conf
            while not data_in.is_empty():
                if len(data_to_write) > 0:
                    data_to_write += "\n"
                line = ""
                for j in range(32):  # align with 512b. word=16b=32words in 512b
                    if data_in.is_empty():
                        line = to_hex(0, 16) + line
                    else:
                        line = to_hex(data_in.get(), 16) + line
                data_to_write = data_to_write + line
                file = correct_directory_path(
                    search_a_path('verilog_simul/input_files',
                                  paths)) + str(i) + ".txt"
                input_files.append(file)
                save_file(file, data_to_write, "w")
        # create the HW verilog file
        cgra_acc_testbench_verilog = \
            create_testbench_sim(cgra_acc,
                                 tam_input_data,
                                 input_files).to_verilog()
        method = "w"
        file = correct_directory_path(
            search_a_path("verilog_simul/verilog_src",
                          paths)) + "test_bench.v"
        save_file(file, cgra_acc_testbench_verilog, method)

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
