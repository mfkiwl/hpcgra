# Class for a basic node, that will be inherited for other nodes
# Jeronimo Costa Penha 2021/03/09

import queue


class Node:
    name = ""
    v_inputs = []
    inputs = []
    n_inputs = 0
    output = 0
    v_output = 0

    # initialization: Defines the name and the number of inputs that the node
    # has.
    def __init__(self, name: str, n_inputs: int):
        self.name = name
        self.set_n_inputs(n_inputs)
        self.v_output = 0

    # returns the number of inputs defined
    def get_n_inputs(self):
        return self.n_inputs

    # sets the number of inputs for the node. It cleans the content of queues
    def set_n_inputs(self, n_inputs: int):
        if n_inputs <= 0:
            n_inputs = 1
        self.inputs = []
        self.v_inputs = []
        self.n_inputs = n_inputs
        for i in range(self.n_inputs):
            self.inputs.append(queue.Queue())
            self.v_inputs.append(queue.Queue())

    # Return the array of node's inputs
    def get_inputs(self) -> tuple[list[int], list[int]]:
        return self.inputs, self.v_inputs

    def get_output(self):
        return self.output, self.v_output

    # Queue a new input in the indicated queue with its valid signal
    def queue_input(self, data, v_data: int, queue_number):
        self.inputs[queue_number].put(data)
        self.v_inputs[queue_number].put(v_data)

    # The user's main function. Here is the main code for the node. It defines
    # it's response
    def execute(self):
        if self.inputs[0].qsize() > 0:
            self.output = self.inputs[0].get()
            self.v_output = self.v_inputs[0].get()

    #def to_string(self):
    #    print("Name: " + self.name + ", n_inputs: " + str(len(self.inputs)) +
    #          ", output_data: " + self.output + ", v_output: " + self.v_output)

# n_inputs = 10
# a = Node("node1", n_inputs)

# for i in range(n_inputs):
#    for j in range(len(a.inputs)):
#        a.queue_input(i, 1, j)
# for i in range(len(a.inputs)):
#    a.queue_input(i, 2, i)

# while a.v_output != 2:
#    a.execute()
#    if a.v_output == 1:
#        print(a.output)
