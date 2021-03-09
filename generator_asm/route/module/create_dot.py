import networkx as nx

def create_dot(g, dict_breadth, vector_results_router, arch, size, device):
    
    name_arch = "mesh"
    if arch == 1:
        name_arch = "one_hop"

    #best_index = 0
    #value_weight = vector_results_router[0][0]
    for i in range(len(vector_results_router)):
        #if value_weight > vector_results_router[i][0]:
        #    value_weight = vector_results_router[i][0]
        #    best_index = i

        new_g = g.copy()
        
        ports = {}
        for e0, e1 in new_g.edges():
            key = str(dict_breadth[str(e0)]) + "_" + str(dict_breadth[str(e1)])
            new_g[e0][e1]['weight'] = vector_results_router[i][1][key]

            if e1 not in ports:
                ports[e1] = 0
            else:
                ports[e1] += 1
            
            new_g[e0][e1]['port'] = ports[e1]
    
        path_dot = "dot_result/" + str(g) + "_" + device + "_" + name_arch + "_" + str(size) + "_" + str(i) +".dot"

        nx.networkx.drawing.nx_pydot.write_dot(new_g, path_dot)