import sys, time
import networkx as nx
import math
import numpy as np
from module.read_inputs import read_list 
from module.read_inputs import read_results
from module.create_index import get_index
from module.routing_algorithm import *
from module.buffer_algorithm import create_buffer
from module.create_dot import create_dot
from module.get_tree import get_tree
from module.get_costs import get_costs
from module.generate_assembly import cgra_assembly
from module.preprocessing import preprocessing

def print_place(place, GRID_SIZE, dict_inv):

    for i in range(len(place)):
        if i % GRID_SIZE == 0:
            print()
        if int(place[i]) == -1:
            print("%7s " %("NONE"), end="")
        else:
            print("%7s " %(dict_inv[place[i]]), end="")
    print("\n")

'''
    Funtion main
'''
if __name__ == "__main__":
    
    if len(sys.argv) > 3:
        arch = int(sys.argv[1])
        dot = sys.argv[2]
        dot_list = sys.argv[3]
        result = sys.argv[4]
    else:
        print("python3 routing.py <ARCH> <name.dot> <name_list.in> <results_place.in>\n")
        exit(0)

    name = result.split("/")[-1].split(".")[0]

    new_g = nx.DiGraph(nx.drawing.nx_pydot.read_dot(dot))
    g = preprocessing(new_g.copy())

    dict_breadth, dict_inv = get_index(g)

    NODE_SIZE, n_edge, edges = read_list(dot_list)
    
    v_place = read_results(result)
    
    GRID_SIZE = math.ceil(math.sqrt(NODE_SIZE))
    TOTAL_GRID_SIZE = GRID_SIZE * GRID_SIZE

    vector_dic_cost, vector_pos, vector_sum_total, dict_cost_wire = get_costs(v_place, NODE_SIZE, GRID_SIZE, dict_inv, edges, arch)

    edges_neighood = []

    for i in range(len(vector_dic_cost)):
        aux1 = []
        for j in range(0, len(edges), 2):
            key = edges[j] + "_" + edges[j+1]
            cost = vector_dic_cost[i][key]
            if cost == 0:
                aux1.insert(0, edges[j])
                aux1.insert(1, edges[j+1])
            else: # insert considering cost wire
                if len(aux1) == 0: # if aux is empty
                    aux1.append(edges[j])
                    aux1.append(edges[j+1])
                else: # if aux isn't empty
                    for k in range(0,len(aux1),2):
                        new_key = aux1[k] + "_" + aux1[k+1]
                        new_cost = vector_dic_cost[i][key]
                        if cost < new_cost or k == len(aux1)-2:
                            aux1.insert(k, edges[j])
                            aux1.insert(k+1, edges[j+1])               
        edges_neighood.append(aux1)

    place_router = []
    path_router = []
    pe = []

    TOTAL_SOLUTION = len(v_place)

    begin = time.time()
    if arch == 0:
        for i in range(TOTAL_SOLUTION):
            dic_path, dic_pe = {}, {}
            bool_routing = False
            grid = np.full((TOTAL_GRID_SIZE,4,1), -1, dtype=int)
            bool_routing = routing_mesh(edges_neighood[i], NODE_SIZE, GRID_SIZE, TOTAL_GRID_SIZE, vector_pos[i], grid, vector_dic_cost[i], dic_path, dic_pe)
            if bool_routing:
                place_router.append([v_place[i], grid, vector_dic_cost[i], dic_path])
                pe.append(dic_pe)
    else: # arch 1hop
        for i in range(TOTAL_SOLUTION):
            dic_path, dic_pe = {}, {}
            bool_routing = False
            grid = np.full((GRID_SIZE*GRID_SIZE,4,2), -1, dtype=int)
            bool_routing = routing_1hop(edges_neighood[i], NODE_SIZE, GRID_SIZE, TOTAL_GRID_SIZE, vector_pos[i], grid, vector_dic_cost[i], dic_path, dic_pe)
            if bool_routing:
                place_router.append([v_place[i], grid, vector_dic_cost[i], dic_path])
                pe.append(dic_pe)

    time_routing = time.time() - begin

    total_route_percent = len(place_router)*100/len(v_place)
    total_not_route_percent = 100 - total_route_percent

    print("Total route        : %6.2f" %total_route_percent)
    print("Total not route    : %6.2f" %total_not_route_percent)
    print("Time spent (s)     : %7.3f\n" %time_routing)
    
    # buffer algorithm
    print("BUFFER EXECUTING")

    vector_dic_cost = []
    for i in range(len(place_router)):
        vector_dic_cost.append(place_router[i][2])

    dict_tree = get_tree(g)
    
    begin = time.time()
    buffer, vector_dict_tree = create_buffer(g, dict_tree.copy(), dict_breadth, vector_dic_cost)
    time_buffer = time.time() - begin

    print("Time spent (s)     : %7.3f\n" %time_buffer)

    # escolher o melhor buffer e melhor custo de fios
    min_buffer, min_wire_cost = 9999, 9999
    
    for i in range(len(buffer)):
        max_buffer = -1
        for j in range(0, n_edge):
            key = str(edges[2*j]) + "_" + str(edges[2*j+1])
            if max_buffer < buffer[i][key]:
                max_buffer = buffer[i][key]
        
        max_value_tree = max(vector_dict_tree[i].values())
        if max_buffer < min_buffer:
            min_buffer = max_buffer
            min_index = i
            min_wire_cost = max_value_tree
        elif max_buffer == min_buffer and max_value_tree < min_wire_cost:
            min_index = i
            min_wire_cost = max_value_tree

    print("Cost buffer: %d indice: %d\n" %(min_buffer, min_index))

    print_place(place_router[min_index][0], GRID_SIZE, dict_inv)
    cgra_assembly(new_g, buffer[min_index], place_router[min_index][3], edges, dict_inv, dict_breadth, GRID_SIZE, pe[min_index], name)