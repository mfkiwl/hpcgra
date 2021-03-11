# Class for the ADD node. This node returns the sum of the input values
# Jeronimo Costa Penha 2021/03/09

from simul_dot.nodes.node import Node


# TODO DESCRIPTION AND COMMENTS
# TODO TO_STRING

class AddNode(Node):

    def execute(self):
        sum_to_out = 0
        for i in range(len(self._inputs)):
            sum_to_out += self._inputs[i].get()
        self._output = sum_to_out
