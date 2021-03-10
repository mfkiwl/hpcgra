# Class for the ADD node. This node returns the sum of the input values
# Jeronimo Costa Penha 2021/03/09

from nodes.Node import Node


class AddNode(Node):

    # Execute method overrited to do what we need, that is pass the input to
    # the output
    def execute(self):
        for i in self.inputs:
            if i.qsize() <= 0:
                return
        sum_to_out = 0
        not_valid = False
        for i in range(len(self.inputs)):
            valid = self.v_inputs[i].get()
            if valid == 0:
                self.output = self.inputs[i].get()
                self.v_output = 0
                not_valid = True
            if valid == 2:
                self.output = self.inputs[i].get()
                self.v_output = 2
                not_valid = True
            if valid == 1:
                sum_to_out += self.inputs[i].get()
        if not_valid:
            return
        self.v_output = 1
        self.output = sum_to_out

# n_inputs = 10
# a = AddNode("add1", n_inputs)

# for i in range(n_inputs):
#    for j in range(len(a.inputs)):
#        a.queue_input(i, 1, j)
# for i in range(len(a.inputs)):
#    a.queue_input(i, 2, i)

# while a.v_output != 2:
#    a.execute()
#    if a.v_output == 1:
#        print(a.output)
