def get_tree(g):

    dict_tree = {}

    OPEN, CLOSED = [[],[]], [[],[]]
    # get the node inputs
    for n in g.nodes():
        for k in range(2):
            if g.in_degree(n) == 0:
                OPEN[k].insert(0, n)
                dict_tree[n] = 0

    for k in range(len(OPEN)):
        while len(OPEN[k]) > 0 :
            node = OPEN[k].pop(0)
            CLOSED[k].append(node)

            maior = -1
            for no in list(g.successors(node)):
                #print(no)
                if no in dict_tree:
                    if dict_tree[no] < dict_tree[node] + 1 and no != node:
                        dict_tree[no] = dict_tree[node] + 1
                        if maior < dict_tree[no]:
                            maior = dict_tree[no]
                else:
                    dict_tree[no] = dict_tree[node] + 1
                    if maior < dict_tree[no]:
                        maior = dict_tree[no]
                if no not in OPEN[k] and no not in CLOSED[k]:
                    OPEN[k].append(no)
            
            # update son node, with the great than nodes
            for no in list(g.successors(node)):
                if no != node and maior != -1:
                    dict_tree[no] = maior
    
    return dict_tree

def get_tree_inverse(g):
    dict_tree = {}

    OPEN, CLOSED = [[],[]], [[],[]]
    # get the node inputs
    for n in g.nodes():
        for k in range(2):
            if g.out_degree(n) == 0:
                OPEN[k].insert(0, n)
                dict_tree[n] = 0

    for k in range(len(OPEN)):
        while len(OPEN[k]) > 0 :
            son = OPEN[k].pop(0)
            CLOSED[k].append(son)

            maior = -1
            for dad in list(g.predecessors(son)):
                #print(no)
                if dad in dict_tree:
                    if dict_tree[dad] < dict_tree[son] + 1 and dad != son:
                        dict_tree[dad] = dict_tree[son] + 1
                        if maior < dict_tree[dad]:
                            maior = dict_tree[dad]
                else:
                    dict_tree[dad] = dict_tree[son] + 1
                    if maior < dict_tree[dad]:
                        maior = dict_tree[dad]
                if dad not in OPEN[k] and dad not in CLOSED[k]:
                    OPEN[k].append(dad)
            
            # update son node, with the great than nodes
            for dad in list(g.predecessors(son)):
                if dad != son and maior != -1:
                    dict_tree[dad] = maior
    #print(dict_tree)
    return dict_tree