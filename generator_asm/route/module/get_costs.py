from random import randint

def local_mesh(pos_a_x, pos_a_y, pos_b_x, pos_b_y):

    diff_x = abs(pos_a_x-pos_b_x)
    diff_y = abs(pos_a_y-pos_b_y)

    if diff_x + diff_y == 0:
        return 0
    else:
        return diff_x + diff_y - 1

def local_1hop(pos_a_x, pos_a_y, pos_b_x, pos_b_y):

    diff_x = abs(pos_a_x-pos_b_x)
    diff_y = abs(pos_a_y-pos_b_y)

    if diff_x + diff_y == 0:
        return 0
    else:
        return diff_x//2 + diff_y//2 + diff_x%2 + diff_y%2 - 1

table1hop = [[0,  0,  0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7],  
 [0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8],  
 [0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8],  
 [1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9],  
 [1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9],  
 [2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10],  
 [2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10],  
 [3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11],  
 [3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11],  
 [4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12],  
 [4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12],  
 [5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13],  
 [5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13],  
 [6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14],  
 [6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14],  
 [7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15],  
 [7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15]]

tablemesh = [[0,  0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9],  
 [0,  1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9],  
 [1,  1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10],  
 [1,  2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10],  
 [2,  2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11],  
 [2,  3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11],  
 [3,  3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12],  
 [3,  4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12],  
 [4,  4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13],  
 [4,  5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13],  
 [5,  5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14],  
 [5,  6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14],  
 [6,  6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15],  
 [6,  7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15],  
 [7,  7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16],  
 [7,  8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16],  
 [8,  8,  9,  9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17]]

def local_chess(pos_a_x, pos_a_y, pos_b_x, pos_b_y):

    distManhattanJ = abs(pos_a_y-pos_b_y)
    distManhattanI = abs(pos_a_x-pos_b_x)

    diff_x = abs(pos_a_x-pos_b_x)
    diff_y = abs(pos_a_y-pos_b_y)

    if diff_x + diff_y == 0:
        return 0
    else:
        if abs(pos_a_x-pos_a_y) % 2 == 0: # par
            return table1hop[distManhattanI][distManhattanJ]
        else:
            return tablemesh[distManhattanI][distManhattanJ]

tablehex = [[0,  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],  
 [0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], 
 [1,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],  
 [2,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],  
 [3,  3,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],   
 [4,  4,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],  
 [5,  5,  5,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],  
 [6,  6,  6,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],  
 [7,  7,  7,  7,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],  
 [8,  8,  8,  8,  8,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],  
 [9,  9,  9,  9,  9,  9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], 
 [10,10, 10, 10, 10, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],  
 [11,11, 11, 11, 11, 11, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26],
 [12,12, 12, 12, 12, 12, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],  
 [13,13, 13, 13, 13, 13, 13, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],   
 [14,14, 14, 14, 14, 14, 14, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],  
 [15,15, 15, 15, 15, 15, 15, 15, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
 [16,16, 16, 16, 16, 16, 16, 16, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
 [17,17, 17, 17, 17, 17, 17, 17, 17, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]]

def local_hex(pos_a_x, pos_a_y, pos_b_x, pos_b_y):

    distManhattanJ = abs(pos_a_y-pos_b_y)
    distManhattanI = abs(pos_a_x-pos_b_x)

    return tablehex[distManhattanI][distManhattanJ]

def get_costs(v_results, n_node, GRID_SIZE, dict_inv, edges, N_STRATEGY):
    vector_dic_cost = []

    vector_pos = []
    
    vector_sum_total = [9999, -1] # (value, index)
    
    dict_cost_wire = {}
    
    for k in range(len(v_results)):
        positions = []
        dict_cost = {}
        for i in range(n_node):
            find = False
            for j in range(len(v_results[k])):
                if str(i) == v_results[k][j]:
                    row = j // GRID_SIZE
                    col = j % GRID_SIZE
                    positions.append((row, col))
                    find = True
                    break
            if not find:
                print("Not found %d line %d" %(i,k))
                continue

        maior_value = 0
        sum_total = 0
        vector_pos_local = {}
        for i in range(0, len(edges), 2):
            key = edges[i] + "_" + edges[i+1]
            pos_a_x = positions[int(edges[i])][0]
            pos_a_y = positions[int(edges[i])][1]
            pos_b_x = positions[int(edges[i+1])][0]
            pos_b_y = positions[int(edges[i+1])][1]

            vector_pos_local[str(edges[i])] = [positions[int(edges[i])][0], positions[int(edges[i])][1]]
            vector_pos_local[str(edges[i+1])] = [positions[int(edges[i+1])][0], positions[int(edges[i+1])][1]]
            
            if N_STRATEGY == 0:
                sum_local = local_mesh(pos_a_x, pos_a_y, pos_b_x, pos_b_y)
            elif N_STRATEGY == 1:
                sum_local = local_chess(pos_a_x, pos_a_y, pos_b_x, pos_b_y)
            elif N_STRATEGY == 2:
                sum_local = local_1hop(pos_a_x, pos_a_y, pos_b_x, pos_b_y)
            elif N_STRATEGY == 3:
                sum_local = local_hex(pos_a_x, pos_a_y, pos_b_x, pos_b_y)
            
            if maior_value < sum_local:
                maior_value = sum_local
            
            sum_total += sum_local

            #print("%2d -> %2d cost: %d" %(int(edges[i]), int(edges[i+1]), sum_mesh_local))

            dict_cost[key] = sum_local
        vector_dic_cost.append(dict_cost)
        vector_pos.append(vector_pos_local)

        if sum_total not in dict_cost_wire:
            dict_cost_wire[sum_total] = 1
        else:
            dict_cost_wire[sum_total] += 1

        if sum_total < vector_sum_total[0]:
            vector_sum_total[0] = sum_total
            vector_sum_total[1] = k
        
        #print("sum = %d, index = %d" %(sum_total_mesh, k))

    return vector_dic_cost, vector_pos, vector_sum_total, dict_cost_wire

def get_costs_vpr(v_results, n_node, GRID_SIZE, dict_inv, edges, N_STRATEGY):
    vector_dic_cost = []

    vector_pos = {}
    
    vector_sum_total = [9999, -1] # (value, index)
    
    dict_cost_wire = {}

    #print(edges)
    #print(n_node)
    #print(v_results[0])
    
    for k in range(len(v_results)):
        positions = []
        dict_cost = {}
        for i in range(n_node):
            find = False
            for j in range(len(v_results[k])):
                if str(i) == v_results[k][j]:
                    row = j // GRID_SIZE
                    col = j % GRID_SIZE
                    positions.append((row, col))
                    find = True
                    break
                elif "|" in v_results[k][j]:
                    value = v_results[k][j].split("|")
                    for l in value:
                        if str(i) == l:
                            row = j // GRID_SIZE
                            col = j % GRID_SIZE
                            positions.append((row, col))
                            find = True
                            break
                    if find:
                        break
            if not find:
                #row = randint(0, GRID_SIZE) 
                #col = randint(0, GRID_SIZE) 
                #positions.append((row, col))
                print("Not found %d line %d" %(i,k+1))
                continue

        maior_value = 0
        sum_total = 0

        for i in range(0, len(edges), 2):
            key = edges[i] + "_" + edges[i+1]
            pos_a_x = positions[int(edges[i])][0]
            pos_a_y = positions[int(edges[i])][1]
            pos_b_x = positions[int(edges[i+1])][0]
            pos_b_y = positions[int(edges[i+1])][1]

            vector_pos[dict_inv[edges[i]]] = [positions[int(edges[i])][0], positions[int(edges[i])][1]]
            vector_pos[dict_inv[edges[i+1]]] = [positions[int(edges[i+1])][0], positions[int(edges[i+1])][1]]
            
            if N_STRATEGY == 0:
                sum_local = local_mesh(pos_a_x, pos_a_y, pos_b_x, pos_b_y)
            elif N_STRATEGY == 1:
                sum_local = local_chess(pos_a_x, pos_a_y, pos_b_x, pos_b_y)
            elif N_STRATEGY == 2:
                sum_local = local_1hop(pos_a_x, pos_a_y, pos_b_x, pos_b_y)
            elif N_STRATEGY == 3:
                sum_local = local_hex(pos_a_x, pos_a_y, pos_b_x, pos_b_y)
            
            if maior_value < sum_local:
                maior_value = sum_local
            
            sum_total += sum_local

            #print("%2d -> %2d cost: %d" %(int(edges[i]), int(edges[i+1]), sum_local))

            dict_cost[key] = sum_local
        vector_dic_cost.append(dict_cost)

        if sum_total not in dict_cost_wire:
            dict_cost_wire[sum_total] = 1
        else:
            dict_cost_wire[sum_total] += 1

        if sum_total < vector_sum_total[0]:
            vector_sum_total[0] = sum_total
            vector_sum_total[1] = k
        
        #print("sum = %d, index = %d" %(sum_total_mesh, k))

    return vector_dic_cost, vector_pos, vector_sum_total, dict_cost_wire
