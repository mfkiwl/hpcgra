# Class for the Input node. This node creates a series of data to the be
# process in the dataflow.
# Jeronimo Costa Penha 2021/03/10
from random import randint

from src.simul.simul_dot.nodes.node import Node
from src.simul.util.simul_util_functions import correct_directory_path, save_file, generate_input_sequence


# TODO DESCRIPTION AND COMMENTS
# TODO TO_STRING

class InputNode(Node):

    def __init__(self, name: str, type_of_generation: int, tam_in: int):
        super().__init__(name, 1)
        self._data_in = generate_input_sequence(type_of_generation, tam_in)

    def execute(self):
        if self._data_in.get_size() > 0:
            self._output = self._data_in.get()
            self._v_output = 1
        else:
            self._v_output = 2

    def pre_execute(self):
        self.execute()
