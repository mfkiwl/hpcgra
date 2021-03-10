# Class for the Input node. This node creates a series of data to the be
# process in the dataflow.
# Jeronimo Costa Penha 2021/03/10
import queue
from random import random, randint

from nodes.Node import Node


class InputNode(Node):
    data_in = queue.Queue()

    # Constructor for the pass node
    def __init__(self, name: str, type_of_generation: int, tam_in: int, generated_file_path: str):
        self.name = name
        self.set_n_inputs(1)
        self.data_in = queue.Queue()
        content = ""
        if type_of_generation == 0:
            for i in range(tam_in):
                n = 1
                self.data_in.put(n)
                content += str(n) + "\n"
        elif type_of_generation == 1:
            for i in range(tam_in):
                n = i + 1
                self.data_in.put(n)
                content += str(n) + "\n"
        elif type_of_generation == 2:
            for i in range(tam_in):
                n = randint(1, 65535)
                self.data_in.put(n)
                content += str(n) + "\n"
        self.save_file(generated_file_path, content)

    def save_file(self, file_path, content):
        file = open(file_path + self.name + "_input.txt", 'w')
        file.writelines(content)
        file.close()

    # Execute method overrited to do what we need, that is pass the input to
    # the output
    def execute(self):
        if self.data_in.qsize() > 0:
            self.output = self.data_in.get()
            self.v_output = 1
        else:
            self.v_output = 2

# a = InputNode("in1", 1, 10)
# while a.v_output!=2:
#    a.execute()
#    if a.v_output==1:
#        print(a.output)
