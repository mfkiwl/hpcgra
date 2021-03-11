# Class for the Output node. This node receives data and writes in files with
# it's name
# Jeronimo Costa Penha 2021/03/10

# TODO DESCRIPTION AND COMMENTS
# TODO TO_STRING

from util.Queue import Queue
from nodes.Node import Node


class OutputNode(Node):

    def __init__(self, name: str, output_file_path: str):
        super().__init__(name, 1)
        self._done = 0
        self._file_path = output_file_path
        self._data_out = Queue()

    def execute(self):
        self._data_out.put(self._inputs[0].get())

    def pre_execute(self):
        if self.is_some_input_empty():
            return
        elif self.check_not_valid():
            return
        if self.check_done():
            file = open(self._file_path + self._name + "_output.txt", "w")
            content = ""
            while self._data_out.get_size() > 0:
                content += str(self._data_out.get()) + "\n"
            file.writelines(content)
            file.close()
            self._done = 1
            return
        for i in range(len(self._inputs)):
            self._v_inputs[i].get()
        self.execute()

    def get_done(self):
        return self._done
