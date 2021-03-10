from nodes.AddNode import AddNode
from nodes.InputNode import InputNode
from nodes.OutputNode import OutputNode
from dot.DotInterpreter import DotInterpreter


class DataFlow:
    di = ""
    output_nodes = []
    nodes = {}
    edges = {}
    done = 0

    def __init__(self, di: DotInterpreter):
        self.di = di
        self.done = 0

    def get_done(self):
        return self.done

    def do_clock(self):
        for e in self.edges:
            producer = self.nodes[e[0]]
            consumer = self.nodes[e[1]]
            port = e[2]
            data, valid = producer.get_output()
            consumer.queue_input(data, valid, port)
        for n in self.nodes:
            self.nodes[n].execute()
        for o in self.output_nodes:
            if o.done == 0:
                return
        self.done = 1

    def create_dataflow(self, type_of_input_generation: int,
                        tam_input_data: int, generated_files_path: str):
        nodes = self.di.get_nodes()
        edges = self.di.get_edges()
        opcodes = self.di.get_opcodes()
        n_input_per_node = self.di.get_n_input_per_node()
        edges_ports = self.di.get_edges_ports()
        self.nodes = {}
        for n in nodes:
            node = ""
            if opcodes[n] == 'input':
                node = InputNode(n, type_of_input_generation, tam_input_data, generated_files_path)
            elif opcodes[n] == 'output':
                node = OutputNode(n, generated_files_path)
                self.output_nodes.append(node)
            elif opcodes[n] == 'add':
                node = AddNode(n, n_input_per_node[n])
            self.nodes[n] = node
        self.edges = []
        for e in edges:
            list = []
            list.append(e[0])
            list.append(e[1])
            list.append(edges_ports[e])
            self.edges.append(list)

# di = DotInterpreter("../vector_sum.dot")
# d = DataFlow(di)
# d.create_dataflow(1, 10, "../")
