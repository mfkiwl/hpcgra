# Class for a basic node, that will be inherited for other nodes
# Jeronimo Costa Penha 2021/03/09

from util.queue import Queue


# TODO DESCRIPTION AND COMMENTS
# TODO TO_STRING

class Node:

    # initialization: Defines the name and the number of inputs that the node
    # has.
    def __init__(self, name: str, n_inputs: int):
        self._name = name
        self._v_output = 0
        self._output = 0
        self._v_inputs = []
        self._inputs = []
        self.set_n_inputs(n_inputs)

    # sets the number of inputs for the node. It cleans the content of queues
    def set_n_inputs(self, n_inputs: int):
        if n_inputs <= 0:
            n_inputs = 1
        self._inputs = []
        self._v_inputs = []
        for i in range(n_inputs):
            self._inputs.append(Queue())
            self._v_inputs.append(Queue())

    # Return the array of node's inputs
    def get_inputs(self) -> tuple[list[Queue], list[Queue]]:
        return self._inputs, self._v_inputs

    def get_output(self):
        return self._output, self._v_output

    # Queue a new input in the indicated queue with its valid signal
    def queue_input(self, data, v_data: int, queue_number):
        self._inputs[queue_number].put(data)
        self._v_inputs[queue_number].put(v_data)

    # The user's main function. Here is the main code for the node. It defines
    # it's response
    def execute(self):
        pass

    def get_new_valid_signals(self):
        new_valid_signals = []
        if self.is_some_input_empty():
            return new_valid_signals
        for i in self._v_inputs:
            new_valid_signals.append(i.get_peek())
        return new_valid_signals

    def is_some_input_empty(self):
        for i in self._v_inputs:
            if i.is_empty():
                return True
        return False

    def check_not_valid(self):
        new_valid_signals = self.get_new_valid_signals()
        if len(new_valid_signals) <= 0:
            return True
        not_valid = False
        for i in range(len(new_valid_signals)):
            if new_valid_signals[i] == 0:
                not_valid = True
                self._inputs[i].get()
                self._v_inputs[i].get()
        if not_valid:
            return True
        return False

    def check_done(self):
        new_done_signals = self.get_new_valid_signals()
        if len(new_done_signals) <= 0:
            return False
        done = False
        for i in range(len(new_done_signals)):
            if new_done_signals[i] == 2:
                self._output = self._inputs[i].get()
                self._v_output = self._v_inputs[i].get()
                done = True
        if done:
            return True
        return False

    def pre_execute(self):
        self._output = 0
        self._v_output = 0
        if self.is_some_input_empty():
            return
        elif self.check_not_valid():
            return
        if self.check_done():
            return
        for i in range(len(self._inputs)):
            self._v_inputs[i].get()
        self._v_output = 1
        self.execute()
