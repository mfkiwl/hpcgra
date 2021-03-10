# Class for the Output node. This node receives data and writes in files with
# it's name
# Jeronimo Costa Penha 2021/03/10
import queue

from nodes.Node import Node


class OutputNode(Node):
    data_out = queue.Queue()
    done = 0
    file_path = ""

    # Constructor for the pass node
    def __init__(self, name: str, file_path: str):
        self.name = name
        self.set_n_inputs(1)
        self.done = 0
        self.file_path = file_path

    # Execute method overrited to do what we need, that is pass the input to
    # the output
    def execute(self):
        if self.inputs[0].qsize() > 0:
            valid = self.v_inputs[0].get()
            data = self.inputs[0].get()
            if valid == 1:
                self.data_out.put(data)
            elif valid == 2:
                file = open(self.file_path + self.name + "_output.txt", "w")
                content = ""
                while self.data_out.qsize() > 0:
                    content += str(self.data_out.get()) + "\n"
                file.writelines(content)
                file.close()
                self.done = 1

    #def to_string(self):
    #    print("Name: " + self.name + ", n_inputs: " + len(self.inputs) +
    #          ", input_data: " + self.output + ", v_input: " + self.v_output)

# a = OutputNode("out1", "teste.txt")
# for i in range(3):
#    a.queue_input(i,1,0)
# a.queue_input(0,2,0)
# while a.done != 1:
#    a.execute()
