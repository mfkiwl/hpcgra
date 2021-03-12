# Class for the Input node. This node creates a series of data to the be
# process in the dataflow.
# Jeronimo Costa Penha 2021/03/10
from random import randint

from src.simul.simul_dot.nodes.node import Node
from src.simul.util.os_util_functions import correct_directory_path, save_file
from src.simul.util.queue import Queue


# TODO DESCRIPTION AND COMMENTS
# TODO TO_STRING

class InputNode(Node):

    def __init__(self, name: str, type_of_generation: int, tam_in: int, generated_file_path: str):
        super().__init__(name, 1)
        self._data_in = Queue()
        content = ""
        if type_of_generation == 0:
            for i in range(tam_in):
                n = 1
                self._data_in.put(n)
                content += str(n) + "\n"
        elif type_of_generation == 1:
            for i in range(tam_in):
                n = i + 1
                self._data_in.put(n)
                content += str(n) + "\n"
        elif type_of_generation == 2:
            for i in range(tam_in):
                n = randint(0, 1000)
                self._data_in.put(n)
                content += str(n) + "\n"
        file = correct_directory_path(generated_file_path) + self._name + ".txt"
        method = "w"
        save_file(file, content, method)

    def save_file(self, file_path, content):
        file_path = correct_directory_path(file_path)
        file = open(file_path + self._name + ".txt", 'w')
        file.writelines(content)
        file.close()

    def execute(self):
        if self._data_in.get_size() > 0:
            self._output = self._data_in.get()
            self._v_output = 1
        else:
            self._v_output = 2

    def pre_execute(self):
        self.execute()
