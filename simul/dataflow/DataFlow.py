from nodes.AddNode import AddNode
from nodes.InputNode import InputNode
from nodes.OutputNode import OutputNode
from dot.DotInterpreter import DotInterpreter


# TODO DESCRIPTIONS AND COMMENTS

class DataFlow:

    def __init__(self, di: DotInterpreter):
        self._di = di
        self._done = 0
        self._output_nodes = []
        self._nodes = {}
        self._edges = {}
        self._done = 0

    def get_done(self):
        return self._done

    def tick(self):
        for e in self._edges:
            producer = self._nodes[e[0]]
            consumer = self._nodes[e[1]]
            port = e[2]
            data, valid = producer.get_output()
            consumer.queue_input(data, valid, port)
        for n in self._nodes:
            self._nodes[n].pre_execute()
        for o in self._output_nodes:
            if o._done == 0:
                return
        self._done = 1

    def create_dataflow(self, type_of_input_generation: int,
                        tam_input_data: int, generated_files_path: str):
        nodes = self._di.get_nodes()
        edges = self._di.get_edges()
        opcodes = self._di.get_opcodes()
        n_input_per_node = self._di.get_n_input_per_node()
        edges_ports = self._di.get_edges_ports()
        self._nodes = {}
        for n in nodes:
            node = ""
            if opcodes[n] == 'input':
                node = InputNode(n, type_of_input_generation, tam_input_data, generated_files_path)
            elif opcodes[n] == 'output':
                node = OutputNode(n, generated_files_path)
                self._output_nodes.append(node)
            elif opcodes[n] == 'add':
                node = AddNode(n, n_input_per_node[n])
            self._nodes[n] = node
        self._edges = []
        for e in edges:
            objs = []
            objs.append(e[0])
            objs.append(e[1])
            objs.append(edges_ports[e])
            self._edges.append(objs)
