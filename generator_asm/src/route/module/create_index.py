import networkx as nx

def get_index(g):

    # function: breadth-first search
    # dictionary with the order 
    dict_breadth = {}
    dict_breadth_inv = {}

    OPEN = []
    # get the node inputs
    for n in g.nodes():
        if g.in_degree(n) == 0:
            OPEN.insert(0,n)
    CLOSED = []

    count = 0
    while len(OPEN) > 0 :
        node = OPEN.pop()

        dict_breadth[node] = count
        dict_breadth_inv[str(count)] = node
        
        CLOSED.append(node)

        for no in list(g.successors(node)):
            if no not in OPEN and no not in CLOSED:
                OPEN.insert(0, no)
        count += 1

    return dict_breadth, dict_breadth_inv   