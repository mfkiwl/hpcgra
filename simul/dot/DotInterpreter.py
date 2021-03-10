# Class responsible for the interpretation of dot file to simulate
# Jeronimo Costa Penha 2021/03/09
from turtle import dot

import networkx as nx


class DotInterpreter:
    dot_file_path = ""
    graph = ""

    # Constructor. Just for set the dot file path
    def __init__(self, dot_file: str):
        self.set_dot_file_path(dot_file)

    def update_graph(self):
        self.graph = nx.DiGraph(nx.drawing.nx_pydot.read_dot(
            self.dot_file_path))

    # Returns the graph dictionary with the contents of dot file
    def get_graph(self) -> nx.DiGraph:
        return self.graph

    def get_opcodes(self):
        opcodes = nx.get_node_attributes(self.get_graph(), 'opcode')
        for k in opcodes:
            opcodes[k] = opcodes[k].replace('"', '')
        return opcodes

    def get_nodes(self):
        return self.get_graph().nodes

    def get_edges(self):
        return nx.edges(self.get_graph())

    def get_edges_ports(self):
        edges_ports = nx.get_edge_attributes(self.get_graph(), 'port')
        for e in edges_ports:
            edges_ports[e] = int(edges_ports[e])
        return edges_ports

    def get_n_input_per_node(self):
        edges = self.get_edges()
        n_input_per_node = {}
        for edge in edges:
            if edge[1] not in n_input_per_node:
                n_input_per_node[edge[1]] = 1
            else:
                n_input_per_node[edge[1]] = n_input_per_node[edge[1]] + 1
        return n_input_per_node

    # Changes the path of the dot file
    def set_dot_file_path(self, dot_file_path):
        self.dot_file_path = dot_file_path
        self.update_graph()

    # returns the actual dot file path
    def get_dot_file_path(self):
        return self.dot_file_path


#a = DotInterpreter("../vector_sum.dot")
#print(a.get_graph())
#print(a.get_nodes())
#print(a.get_opcodes())
#print(a.get_n_input_per_node())
#print(a.get_edges())
#print(a.get_edges_ports())
