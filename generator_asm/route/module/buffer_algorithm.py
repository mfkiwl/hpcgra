def create_buffer(g, dict_tree, dict_breadth, vector_dic_cost):
    OPEN, CLOSED, OUTS = [[],[]], [[],[]], []
    
    vector_dict_tree = []

    for i in range(len(vector_dic_cost)):
        vector_dict_tree.append(dict_tree.copy())

    # get the node inputs and outputs
    for n in g.nodes():
        for k in range(2):
            if g.in_degree(n) == 0:
                OPEN[k].append(n)
        if g.out_degree(n) == 0:
            OUTS.append(n)

    for k in range(2): # confirm update if all node is update (2 times, not necessary more)
        while len(OPEN[k]) > 0 :
            dad = OPEN[k].pop(0)
            CLOSED[k].append(dad)
            for son in list(g.successors(dad)):
                key = str(dict_breadth[dad]) + "_" + str(dict_breadth[son])
                if son not in OPEN[k] and son not in CLOSED[k]:
                    OPEN[k].append(son)
                for i in range(len(vector_dic_cost)):
                    cost_dad = vector_dict_tree[i][dad] + vector_dic_cost[i][key] + 1
                    if (cost_dad > vector_dict_tree[i][son] and son != dad):
                        vector_dict_tree[i][son] = cost_dad

    CLOSED, buffer = [], []

    for i in range(len(vector_dic_cost)):
        buffer.append({})

    while len(OUTS) > 0:
        dad = OUTS.pop(0)
        CLOSED.append(dad)
        for son in list(g.predecessors(dad)):
            key = str(dict_breadth[son]) + "_" + str(dict_breadth[dad])
            if son not in OUTS and son not in CLOSED:
                OUTS.insert(0, son)
            for i in range(len(vector_dic_cost)):
                # Calcule of buffer each edge
                buffer[i][key] = (vector_dict_tree[i][dad] - dict_tree[dad]) - (vector_dict_tree[i][son] - dict_tree[son]) - vector_dic_cost[i][key]
                
    return buffer, vector_dict_tree 

def create_buffer_inverse(g, dict_tree, dict_breadth, vector_dic_cost):
    OPEN, CLOSED, OUTS = [[],[]], [[],[]], []
    
    vector_dict_tree = []

    for i in range(len(vector_dic_cost)):
        vector_dict_tree.append(dict_tree.copy())

    # get the node inputs and outputs
    for n in g.nodes():
        for k in range(2):
            if g.out_degree(n) == 0:
                OPEN[k].append(n)
        if g.in_degree(n) == 0:
            OUTS.append(n)

    for k in range(2): # confirm update if all node is update (2 times, not necessary more)
        while len(OPEN[k]) > 0 :
            son = OPEN[k].pop(0)
            CLOSED[k].append(son)
            for dad in list(g.predecessors(son)):
                key = str(dict_breadth[dad]) + "_" + str(dict_breadth[son])
                if dad not in OPEN[k] and dad not in CLOSED[k]:
                    OPEN[k].append(dad)
                for i in range(len(vector_dic_cost)):
                    cost_son = vector_dict_tree[i][son] + vector_dic_cost[i][key] + 1
                    if (cost_son > vector_dict_tree[i][dad] and son != dad):
                        vector_dict_tree[i][dad] = cost_son

    CLOSED, buffer = [], []

    for i in range(len(vector_dic_cost)):
        buffer.append({})

    while len(OUTS) > 0:
        dad = OUTS.pop(0)
        CLOSED.append(dad)
        for son in list(g.successors(dad)):
            key = str(dict_breadth[dad]) + "_" + str(dict_breadth[son])
            if son not in OUTS and son not in CLOSED:
                OUTS.insert(0, son)
            for i in range(len(vector_dic_cost)):
                # Calcule of buffer each edge
                buffer[i][key] = (vector_dict_tree[i][dad] - dict_tree[dad]) - (vector_dict_tree[i][son] - dict_tree[son]) - vector_dic_cost[i][key]
                
    return buffer, vector_dict_tree 

'''
    buffer_minimize: return the buffer with minimun of buffer (not the best yet)
'''
def buffer_minimize(g, buffer, dict_breadth, dict_tree, vector_dic_cost, strategy):

    CLOSED, OUTS = [], []

    # get the node inputs and outputs
    for n in g.nodes():
        if g.out_degree(n) == 0:
            OUTS.append(n)
    
    buffer_begin = []
    for i in range(len(buffer)):
        buffer_begin.append({})

    while len(OUTS) > 0:
        dad = OUTS.pop(0)
        CLOSED.append(dad)
        #print(dad, end=' ')
        for son in list(g.predecessors(dad)):
            #print(son, end=' ')
            key = str(dict_breadth[son]) + "_" + str(dict_breadth[dad])
            #print(vector_dict_tree[i][dad], vector_dict_tree[i][son], vector_dict_tree[i][dad] - vector_dict_tree[i][son] - 1 - vector_dic_cost[i][key][0], end=' ')
            if son not in OUTS and son not in CLOSED:
                OUTS.insert(0, son)
            for k in range(len(buffer)):
                if buffer[k][key] > 1:
                    list_son = list(g.predecessors(son))
                    if len(list_son) >= 1:
                        for i in range(len(list_son)):
                            new_key = str(dict_breadth[list_son[i]])  + "_" + str(dict_breadth[son])
                            buffer[k][new_key] = buffer[k][key] // 2 - vector_dic_cost[k][new_key][strategy]
                        buffer[k][key] = buffer[k][key] // 2 + buffer[k][key] % 2 
                # get the buffer begin
                if g.in_degree(son) == 0:
                    #print(dad, dict_tree[dad])
                    new_key = str(dict_breadth[son])  + "_" + str(dict_breadth[dad])
                    buffer_begin[k][son] = dict_tree[dad] #- 1 #- buffer[k][new_key][1]
    return buffer

def buffer_minimize_inverse(g, buffer, dict_breadth, dict_tree, vector_dic_cost, strategy):

    CLOSED, OUTS = [], []

    # get the node inputs and outputs
    for n in g.nodes():
        if g.in_degree(n) == 0:
            OUTS.append(n)
    
    buffer_begin = []
    for i in range(len(buffer)):
        buffer_begin.append({})

    while len(OUTS) > 0:
        dad = OUTS.pop(0)
        CLOSED.append(dad)
        #print(dad, end=' ')
        for son in list(g.successors(dad)):
            #print(son, end=' ')
            key = str(dict_breadth[dad]) + "_" + str(dict_breadth[son])
            #print(vector_dict_tree[i][dad], vector_dict_tree[i][son], vector_dict_tree[i][dad] - vector_dict_tree[i][son] - 1 - vector_dic_cost[i][key][0], end=' ')
            if son not in OUTS and son not in CLOSED:
                OUTS.insert(0, son)
            for k in range(len(buffer)):
                if buffer[k][key] > 1:
                    list_son = list(g.successors(son))
                    if len(list_son) >= 1:
                        for i in range(len(list_son)):
                            new_key = str(dict_breadth[son]) + "_" + str(dict_breadth[list_son[i]])
                            buffer[k][new_key] += buffer[k][key] // 2 - vector_dic_cost[k][new_key][strategy]
                        buffer[k][key] = buffer[k][key] // 2 + buffer[k][key] % 2 
                # get the buffer begin
                #if g.in_degree(son) == 0:
                #    #print(dad, dict_tree[dad])
                #    new_key = str(dict_breadth[son])  + "_" + str(dict_breadth[dad])
                #    buffer_begin[k][son] = dict_tree[dad] #- 1 #- buffer[k][new_key][1]
    return buffer