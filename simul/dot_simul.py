# Simulator for DOT. This project is responsible for test the DOT archives made
# by the team and construct some input-files for the verilog simulation and make
# some output file with the expected result. The objective is to have sure that
# the router is working good.
# Start of develop in 2021/03/09 by Jeronimo Costa Penha.

import sys
from simulation.Simulator import Simulator

# TODO DESCRIPTION AND COMMENTS

if __name__ == "__main__":
    dot_file_path = "./vector_sum2.dot"
    type_of_input_generation = 1
    tam_input_data = 10
    generated_files_path = "./"
    '''
    if len(sys.argv) > 1:
        dot_file_path = sys.argv[1]
        type_of_input_generation = int(sys.argv[2])
        tam_input_data = int(sys.argv[3])
        output_files_path = sys.argv[4]
    else:
        print("Error!\n")
        print("Usage: dot_file_path type_of_input_generation tam_input_data"
              " genereted_files_path")
        exit(0)
    '''
    simulator = Simulator(dot_file_path)
    simulator.start(type_of_input_generation, tam_input_data, generated_files_path)
