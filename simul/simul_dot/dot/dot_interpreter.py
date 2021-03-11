# Class responsible for the interpretation of dot file to simulate
# Jeronimo Costa Penha 2021/03/09

import networkx as nx


# TODO DESCRIPTION AND COMMENTS
# TODO TO_STRING

class DotInterpreter:

    # Constructor. Just for set the dot file path
    def __init__(self, files: []):
        self._files = files
        self._dot_file = self.search_dot_file()
        self._graph = nx.DiGraph(nx.drawing.nx_pydot.read_dot(
            self._dot_file))

    def search_dot_file(self):
        for file in self._files:
            if ".dot" in  file:
                return file
        raise Exception("Error! No .dot file found.")


    def update_graph(self):
        self._graph = nx.DiGraph(nx.drawing.nx_pydot.read_dot(
            self._dot_file))

    # Returns the graph dictionary with the contents of dot file
    def get_graph(self) -> nx.DiGraph:
        return self._graph

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
