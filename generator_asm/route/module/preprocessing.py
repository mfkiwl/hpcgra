import networkx as nx

def preprocessing(g):

    new_g = g.copy()
    dic_opcode = nx.get_node_attributes(g, 'opcode')

    for n in g.nodes():
        #print(dic_opcode[n])
        if dic_opcode[n] == "const":
            #print(n, dic_opcode[n])
            new_g.remove_node(n)

    for e in g.edges():
        if e[0] == e[1]:
            new_g.remove_edge(e[0], e[1])
    return new_g