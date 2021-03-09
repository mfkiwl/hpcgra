import numpy as np

def print_grid(grid, GRID_SIZE, size):
    
    for i in range(GRID_SIZE):
        print("%s T   R   D   L" %(12*" "))
        for j in range(GRID_SIZE):
            print("pe %3d = [" %(i*GRID_SIZE+j), end="")
            for k in range(size):
                print("%4d" %grid[i*GRID_SIZE+j][k], end="")
            print("]")

def verify_routing_mesh(grid_results, list_edge, NODE_SIZE, GRID_SIZE):

    count_sol = 0
    TOTAL_SOLUTIONS = len(grid_results)

    vector_results_router = []
    vector_cost_total_before = []
    routing = []
    cost_wire_total = []
    total_count_neighood = 0

    TOTAL_GRID_SIZE = GRID_SIZE*GRID_SIZE

    for i in range(TOTAL_SOLUTIONS):

        count_neighood = 0

        grid = np.full((TOTAL_GRID_SIZE,4,1), -1, dtype=int)
        
        # get the position on the grid
        positions = []
        dict_router = {}
        cost_total_solution, cost_total_before = 0, 0
        cost_wire = 0
        pos_place = {}
        
        for j in range(NODE_SIZE):
            found = False
            for k in range(len(grid_results[i])):
                if str(j) == grid_results[i][k]:
                    row = k // GRID_SIZE
                    col = k % GRID_SIZE
                    pos_place[str(k)] = j 
                    positions.append((row, col))
                    found = True
                    break
            if not found:
                print("ERROR: The number %d not in the grid result" %j)
                exit(0)
        
        for j in range(0, len(list_edge), 2):

            a = int(list_edge[j])
            b = int(list_edge[j+1])
            pos_a_i = positions[a][0]
            pos_a_j = positions[a][1]
            pos_b_i = positions[b][0]
            pos_b_j = positions[b][1]

            diff_x = abs(pos_a_i-pos_b_i)
            diff_y = abs(pos_a_j-pos_b_j)

            cost_total_before += max(0, diff_x + diff_y - 1)

            if cost_total_before == 0:
                count_neighood += 1
        
        total_count_neighood += count_neighood / (len(list_edge) // 2)

        # verify if is routing
        for j in range(0, len(list_edge), 2):
            a = int(list_edge[j])
            b = int(list_edge[j+1])
            pos_a_i = positions[a][0]
            pos_a_j = positions[a][1]
            pos_b_i = positions[b][0]
            pos_b_j = positions[b][1]

            dist_walk = -1

            diff_i = pos_b_i - pos_a_i
            diff_j = pos_b_j - pos_a_j

            dist_i, dist_j = abs(pos_b_i - pos_a_i), abs(pos_b_j - pos_a_j)

            pos_node_i = pos_a_i
            pos_node_j = pos_a_j
            change = False
            
            #count = 0
            count_per_curr = []
            while dist_i != 0 or dist_j != 0:
                diff_i = pos_b_i - pos_node_i
                diff_j = pos_b_j - pos_node_j
                
                # get the current position node
                pe_curr = pos_node_i * GRID_SIZE + pos_node_j
                count_per_curr.append(pe_curr)

                #print("percuso = ", pe_curr)

                # go to right neighbor
                # [pe], [0 = top, 1 = right, 2 = down, 3 = left], [0 = IN, OUT = 1]
                if diff_j > 0 and pe_curr+1 < (pos_node_i+1)*GRID_SIZE and (grid[pe_curr][1][0] == -1 or grid[pe_curr][1][0] == a) and grid[pe_curr+1][3][0] != a and (pe_curr+1) not in count_per_curr:  # go right
                    grid[pe_curr][1][0] = a
                    pos_node_j += 1
                    change = True
                    #print("VIZ right")
                elif diff_j < 0 and pe_curr-1 >= (pos_node_i)*GRID_SIZE and (grid[pe_curr][3][0] == -1 or grid[pe_curr][3][0] == a) and grid[pe_curr-1][1][0] != a and (pe_curr-1) not in count_per_curr: # go left
                    grid[pe_curr][3][0] = a
                    pos_node_j -= 1
                    change = True
                    #print("VIZ left")
                elif diff_i > 0 and pe_curr+GRID_SIZE < TOTAL_GRID_SIZE and (grid[pe_curr][2][0] == -1 or grid[pe_curr][2][0] == a) and grid[pe_curr+GRID_SIZE][0][0] != a and (pe_curr+GRID_SIZE) not in count_per_curr: # go down
                    grid[pe_curr][2][0] = a
                    pos_node_i += 1
                    change = True
                    #print("VIZ down")
                elif diff_i < 0 and pe_curr-GRID_SIZE >= 0 and (grid[pe_curr][0][0] == -1 or grid[pe_curr][0][0] == a) and grid[pe_curr-GRID_SIZE][2][0] != a and (pe_curr-GRID_SIZE) not in count_per_curr: # go up
                    grid[pe_curr][0][0] = a
                    pos_node_i -= 1
                    change = True
                    #print("VIZ top")
            
                if not change: # change 
                    
                    if pe_curr+1 < (pos_node_i+1)*GRID_SIZE and (grid[pe_curr][1][0] == -1 or grid[pe_curr][1][0] == a) and grid[pe_curr+1][3][0] != a and (pe_curr+1) not in count_per_curr:  # go right
                        grid[pe_curr][1][0] = a
                        pos_node_j += 1
                        change = True
                        #print("right")
                    elif pe_curr-1 >= (pos_node_i)*GRID_SIZE and (grid[pe_curr][3][0] == -1 or grid[pe_curr][3][0] == a) and grid[pe_curr-1][1][0] != a and (pe_curr-1) not in count_per_curr: # go left
                        grid[pe_curr][3][0] = a
                        pos_node_j -= 1
                        change = True
                        #print("left")
                    elif pe_curr+GRID_SIZE < TOTAL_GRID_SIZE and (grid[pe_curr][2][0] == -1 or grid[pe_curr][2][0] == a) and grid[pe_curr+GRID_SIZE][0][0] != a and (pe_curr+GRID_SIZE) not in count_per_curr: # go down
                        grid[pe_curr][2][0] = a
                        pos_node_i += 1
                        change = True
                        #print("down")
                    elif pe_curr-GRID_SIZE >= 0 and (grid[pe_curr][0][0] == -1 or grid[pe_curr][0][0] == a) and grid[pe_curr-GRID_SIZE][2][0] != a and (pe_curr-GRID_SIZE) not in count_per_curr: # go up
                        grid[pe_curr][0][0] = a
                        pos_node_i -= 1
                        change = True
                        #   print("top")
                
                    if not change:
                        #print_grid(grid, GRID_SIZE, 4)
                        change = True
                        break
                
                if not change:
                    change = True
                    #not get solution
                    break
                
                dist_i, dist_j = abs(pos_b_i - pos_node_i), abs(pos_b_j - pos_node_j)
                dist_walk += 1
                change = False

            if change: # stop, give errors
                break
            else:
                cost_total_solution += dist_walk
                key = str(a) + "_" + str(b)
                dict_router[key] = dist_walk
                cost_wire += dist_walk + 1 
                #print("%2d [%2d,%2d][PE %3d] -> %2d [%2d, %2d][PE %3d] Cost_place: %d Cost_route: %d" %(a, pos_a_i, pos_a_j, pos_a_i*GRID_SIZE+pos_a_j, b, pos_b_i, pos_b_j, pos_b_i*GRID_SIZE+pos_b_j, cost_local,dist_walk))
            #print_grid(grid, GRID_SIZE, 4)
        if not change:
            vector_results_router.append([cost_total_solution, dict_router])
            routing.append([pos_place, grid])
            cost_wire_total.append(cost_wire)
            count_sol += 1
    per_rout = count_sol * 100 / TOTAL_SOLUTIONS
    #print(" Number of routing: \t\t%d (%.1f) \n Number of not routing: \t%d (%.1f)" %(count_sol, per_rout, TOTAL_SOLUTIONS-count_sol, 100-per_rout))
    #print(" Wire neighood = %.2f" %(total_count_neighood/TOTAL_SOLUTIONS * 100))
    #print(" Not Wire neighood = %.2f" %((1 - total_count_neighood)/TOTAL_SOLUTIONS * 100))

    #print(vector_results_router)
    return vector_results_router, vector_cost_total_before, routing, cost_wire_total

def verify_routing_1hop(grid_results, list_edge, NODE_SIZE, GRID_SIZE):

    count_sol = 0
    TOTAL_SOLUTIONS = len(grid_results)
    TOTAL_GRID_SIZE = GRID_SIZE*GRID_SIZE

    vector_results_router = []
    vector_cost_total_before = []
    routing = []
    cost_wire_total = []
    total_count_neighood = 0
    total_vizinho = 0
    total_nao_vizinho = 0

    edges_neighhood = []
    edges_not_neighhood = []

    for i in range(TOTAL_SOLUTIONS):

        grid = np.full((TOTAL_GRID_SIZE,4,2), -1, dtype=int)
        
        # get the position on the grid
        positions = []
        pos_place = {}
        dict_router = {}
        cost_total_solution, cost_total_before = 0, 0
        cost_wire = 0
        
        for j in range(NODE_SIZE):
            found = False
            for k in range(len(grid_results[i])):
                if str(j) == grid_results[i][k]:
                    row = k // GRID_SIZE
                    col = k % GRID_SIZE
                    pos_place[str(k)] = j 
                    positions.append((row, col))
                    found = True
                    break
            if not found:
                print("ERROR: The number %d not in the grid result" %j)
                exit(0)
        
        count_neighood = 0
        for j in range(0, len(list_edge), 2):

            a = int(list_edge[j])
            b = int(list_edge[j+1])
            pos_a_i = positions[a][0]
            pos_a_j = positions[a][1]
            pos_b_i = positions[b][0]
            pos_b_j = positions[b][1]

            diff_x = abs(pos_a_i-pos_b_i)
            diff_y = abs(pos_a_j-pos_b_j)

            aux_cost_local = max(0, diff_x//2 + diff_x%2 + diff_y//2 + diff_y%2 - 1)
            cost_total_before += max(0, diff_x//2 + diff_x%2 + diff_y//2 + diff_y%2 - 1)

            if aux_cost_local == 0:
                count_neighood += 1
                edges_neighhood.append(a)
                edges_neighhood.append(b)
            else:
                edges_not_neighhood.append(a)
                edges_not_neighhood.append(b)

        EDGE_SIZE = len(list_edge) // 2
        
        total_vizinho += count_neighood
        total_nao_vizinho += (EDGE_SIZE - count_neighood)
        
        vector_cost_total_before.append(cost_total_before)

        # verify if is routing
        for j in range(0, len(list_edge), 2):
            a = int(list_edge[j])
            b = int(list_edge[j+1])
            pos_a_i = positions[a][0]
            pos_a_j = positions[a][1]
            pos_b_i = positions[b][0]
            pos_b_j = positions[b][1]

            dist_walk = -1

            diff_i = pos_b_i - pos_a_i
            diff_j = pos_b_j - pos_a_j

            dist_i, dist_j = abs(pos_b_i - pos_a_i), abs(pos_b_j - pos_a_j)

            pos_node_i = pos_a_i
            pos_node_j = pos_a_j
            change = False
            
            #count = 0
            count_per_curr = []
            while dist_i != 0 or dist_j != 0:
                diff_i = pos_b_i - pos_node_i
                diff_j = pos_b_j - pos_node_j
                
                # get the current position node
                pe_curr = pos_node_i * GRID_SIZE + pos_node_j
                count_per_curr.append(pe_curr)

                # go to right neighbor
                # [pe], [0 = top, 1 = right, 2 = down, 3 = left], [0 = IN, OUT = 1]
                if diff_j > 0 and dist_j >= 2 and pe_curr+2 < (pos_node_i+1)*GRID_SIZE and (grid[pe_curr][1][1] == -1 or grid[pe_curr][1][1] == a) and grid[pe_curr+2][3][1] != a and (pe_curr+2) not in count_per_curr:  # go right
                    grid[pe_curr][1][1] = a
                    pos_node_j += 2
                    change = True
                    #print("VIZ right 2")
                elif diff_j > 0 and pe_curr+1 < (pos_node_i+1)*GRID_SIZE and (grid[pe_curr][1][0] == -1 or grid[pe_curr][1][0] == a) and grid[pe_curr+1][3][0] != a and (pe_curr+1) not in count_per_curr:  # go right
                    grid[pe_curr][1][0] = a
                    pos_node_j += 1
                    change = True
                    #print("VIZ right 1")
                elif diff_j < 0 and dist_j >= 2 and pe_curr-2 >= (pos_node_i)*GRID_SIZE and (grid[pe_curr][3][1] == -1 or grid[pe_curr][3][1] == a) and grid[pe_curr-2][1][1] != a and (pe_curr-2) not in count_per_curr: # go left
                    grid[pe_curr][3][0] = a
                    pos_node_j -= 2
                    change = True
                    #print("VIZ left 2")
                elif diff_j < 0 and pe_curr-1 >= (pos_node_i)*GRID_SIZE and (grid[pe_curr][3][0] == -1 or grid[pe_curr][3][0] == a) and grid[pe_curr-1][1][0] != a and (pe_curr-1) not in count_per_curr: # go left
                    grid[pe_curr][3][0] = a
                    pos_node_j -= 1
                    change = True
                    #print("VIZ left 1")
                elif diff_i > 0 and dist_i >= 2 and pe_curr+2*GRID_SIZE < TOTAL_GRID_SIZE and (grid[pe_curr][2][1] == -1 or grid[pe_curr][2][1] == a) and grid[pe_curr+2*GRID_SIZE][0][1] != a and (pe_curr+2*GRID_SIZE) not in count_per_curr: # go down
                    grid[pe_curr][2][1] = a
                    pos_node_i += 2
                    change = True
                    #print("VIZ down 2")
                elif diff_i > 0 and pe_curr+GRID_SIZE < TOTAL_GRID_SIZE and (grid[pe_curr][2][0] == -1 or grid[pe_curr][2][0] == a) and grid[pe_curr+GRID_SIZE][0][0] != a and (pe_curr+GRID_SIZE) not in count_per_curr: # go down
                    grid[pe_curr][2][0] = a
                    pos_node_i += 1
                    change = True
                    #print("VIZ down 1")
                elif diff_i < 0 and dist_i >= 2 and pe_curr-2*GRID_SIZE >= 0 and (grid[pe_curr][0][1] == -1 or grid[pe_curr][0][1] == a) and grid[pe_curr-2*GRID_SIZE][2][1] != a and (pe_curr-2*GRID_SIZE) not in count_per_curr: # go up
                    grid[pe_curr][0][0] = a
                    pos_node_i -= 2
                    change = True
                    #print("VIZ top")
                elif diff_i < 0 and pe_curr-GRID_SIZE >= 0 and (grid[pe_curr][0][0] == -1 or grid[pe_curr][0][0] == a) and grid[pe_curr-GRID_SIZE][2][0] != a and (pe_curr-GRID_SIZE) not in count_per_curr: # go up
                    grid[pe_curr][0][0] = a
                    pos_node_i -= 1
                    change = True
                    #print("VIZ top")
            
                if not change: # change 
                    
                    if pe_curr+1 < (pos_node_i+1)*GRID_SIZE and (grid[pe_curr][1][0] == -1 or grid[pe_curr][1][0] == a) and grid[pe_curr+1][3][0] != a and (pe_curr+1) not in count_per_curr:  # go right
                        grid[pe_curr][1][0] = a
                        pos_node_j += 1
                        change = True
                        #print("right 1")
                    elif pe_curr-1 >= (pos_node_i)*GRID_SIZE and (grid[pe_curr][3][0] == -1 or grid[pe_curr][3][0] == a) and grid[pe_curr-1][1][0] != a and (pe_curr-1) not in count_per_curr: # go left
                        grid[pe_curr][3][0] = a
                        pos_node_j -= 1
                        change = True
                        #print("left 1")
                    elif pe_curr+GRID_SIZE < TOTAL_GRID_SIZE and (grid[pe_curr][2][0] == -1 or grid[pe_curr][2][0] == a) and grid[pe_curr+GRID_SIZE][0][0] != a and (pe_curr+GRID_SIZE) not in count_per_curr: # go down
                        grid[pe_curr][2][0] = a
                        pos_node_i += 1
                        change = True
                        #print("down 1")
                    elif pe_curr-GRID_SIZE >= 0 and (grid[pe_curr][0][0] == -1 or grid[pe_curr][0][0] == a) and grid[pe_curr-GRID_SIZE][2][0] != a and (pe_curr-GRID_SIZE) not in count_per_curr: # go up
                        grid[pe_curr][0][0] = a
                        pos_node_i -= 1
                        change = True
                        #print("top 1")
                
                    if not change:
                        #print_grid(grid, GRID_SIZE, 4)
                        change = True
                        break
                
                if not change:
                    change = True
                    #not get solution
                    break
                
                dist_i, dist_j = abs(pos_b_i - pos_node_i), abs(pos_b_j - pos_node_j)
                dist_walk += 1
                change = False

            if change: # stop, give errors
                break
            else:
                cost_total_solution += dist_walk
                key = str(a) + "_" + str(b)
                dict_router[key] = dist_walk
                cost_wire += dist_walk + 1 
                #print("%2d [%2d,%2d][PE %3d] -> %2d [%2d, %2d][PE %3d] Cost_place: %d Cost_route: %d" %(a, pos_a_i, pos_a_j, pos_a_i*GRID_SIZE+pos_a_j, b, pos_b_i, pos_b_j, pos_b_i*GRID_SIZE+pos_b_j, cost_local,dist_walk))
            #print_grid(grid, GRID_SIZE, 4)
        if not change:
            routing.append([pos_place, grid])
            vector_results_router.append([cost_total_solution, dict_router])
            cost_wire_total.append(cost_wire)
            count_sol += 1
        
    per_rout = count_sol * 100 / TOTAL_SOLUTIONS
    total_vizinho = total_vizinho / TOTAL_SOLUTIONS
    total_nao_vizinho = total_nao_vizinho / TOTAL_SOLUTIONS
    EDGE_SIZE = len(list_edge) // 2
    print(" Number of routing: \t\t%d (%.1f) \n Number of not routing: \t%d (%.1f)" %(count_sol, per_rout, TOTAL_SOLUTIONS-count_sol, 100-per_rout))
    print(" Number of edges =      %d" %(EDGE_SIZE))
    print(" avg neighbor =         %.2f" %(total_vizinho))
    print(" avg not neighbor =     %.2f" %(total_nao_vizinho))
    print(" avg per neighbor =     %.2f" %(total_vizinho*100/EDGE_SIZE))
    print(" avg per not neighbor = %.2f" %(total_nao_vizinho*100/EDGE_SIZE))

    #print(vector_results_router)
    return vector_results_router, vector_cost_total_before, routing, cost_wire_total

def routing_mesh(list_edge, NODE_SIZE, GRID_SIZE, TOTAL_GRID_SIZE, positions, grid, dic_cost, dic_path, dic_pe):

    # verify if is routing
    for j in range(0, len(list_edge), 2):
        a = int(list_edge[j])
        b = int(list_edge[j+1])
        key = list_edge[j] + "_" + list_edge[j+1]
        pos_a_i = positions[str(a)][0]
        pos_a_j = positions[str(a)][1]
        pos_b_i = positions[str(b)][0]
        pos_b_j = positions[str(b)][1]

        dic_pe[a] = pos_a_i * GRID_SIZE + pos_a_j
        dic_pe[b] = pos_b_i * GRID_SIZE + pos_b_j

        dic_path[key] = []
        dist_walk = -1

        diff_i, diff_j = pos_b_i - pos_a_i, pos_b_j - pos_a_j
        dist_i, dist_j = abs(pos_b_i - pos_a_i), abs(pos_b_j - pos_a_j)

        pos_node_i, pos_node_j = pos_a_i, pos_a_j
        change = False
        
        count_per_curr = []
        while dist_i != 0 or dist_j != 0:
            diff_i = pos_b_i - pos_node_i
            diff_j = pos_b_j - pos_node_j
            
            # get the current position node
            pe_curr = pos_node_i * GRID_SIZE + pos_node_j
            dic_path[key].append(pe_curr)
            count_per_curr.append(pe_curr)

            # go to right neighbor
            # [pe], [0 = top, 1 = right, 2 = down, 3 = left], [0 = IN, OUT = 1]
            if diff_j > 0 and pe_curr+1 < (pos_node_i+1)*GRID_SIZE and (grid[pe_curr][1][0] == -1 or grid[pe_curr][1][0] == a) and grid[pe_curr+1][3][0] != a and (pe_curr+1) not in count_per_curr:  # go right
                grid[pe_curr][1][0] = a
                pos_node_j += 1
                change = True
                #print("VIZ right 1")
            elif diff_j < 0 and pe_curr-1 >= (pos_node_i)*GRID_SIZE and (grid[pe_curr][3][0] == -1 or grid[pe_curr][3][0] == a) and grid[pe_curr-1][1][0] != a and (pe_curr-1) not in count_per_curr: # go left
                grid[pe_curr][3][0] = a
                pos_node_j -= 1
                change = True
                #print("VIZ left 1")
            elif diff_i > 0 and pe_curr+GRID_SIZE < TOTAL_GRID_SIZE and (grid[pe_curr][2][0] == -1 or grid[pe_curr][2][0] == a) and grid[pe_curr+GRID_SIZE][0][0] != a and (pe_curr+GRID_SIZE) not in count_per_curr: # go down
                grid[pe_curr][2][0] = a
                pos_node_i += 1
                change = True
                #print("VIZ down 1")
            elif diff_i < 0 and pe_curr-GRID_SIZE >= 0 and (grid[pe_curr][0][0] == -1 or grid[pe_curr][0][0] == a) and grid[pe_curr-GRID_SIZE][2][0] != a and (pe_curr-GRID_SIZE) not in count_per_curr: # go up
                grid[pe_curr][0][0] = a
                pos_node_i -= 1
                change = True
                #print("VIZ top 1")
        
            if not change: # change, try a long path  
                
                if pe_curr+1 < (pos_node_i+1)*GRID_SIZE and (grid[pe_curr][1][0] == -1 or grid[pe_curr][1][0] == a) and grid[pe_curr+1][3][0] != a and (pe_curr+1) not in count_per_curr:  # go right
                    grid[pe_curr][1][0] = a
                    pos_node_j += 1
                    change = True
                    #print("right 1")
                elif pe_curr-1 >= (pos_node_i)*GRID_SIZE and (grid[pe_curr][3][0] == -1 or grid[pe_curr][3][0] == a) and grid[pe_curr-1][1][0] != a and (pe_curr-1) not in count_per_curr: # go left
                    grid[pe_curr][3][0] = a
                    pos_node_j -= 1
                    change = True
                    #print("left 1")
                elif pe_curr+GRID_SIZE < TOTAL_GRID_SIZE and (grid[pe_curr][2][0] == -1 or grid[pe_curr][2][0] == a) and grid[pe_curr+GRID_SIZE][0][0] != a and (pe_curr+GRID_SIZE) not in count_per_curr: # go down
                    grid[pe_curr][2][0] = a
                    pos_node_i += 1
                    change = True
                    #print("down 1")
                elif pe_curr-GRID_SIZE >= 0 and (grid[pe_curr][0][0] == -1 or grid[pe_curr][0][0] == a) and grid[pe_curr-GRID_SIZE][2][0] != a and (pe_curr-GRID_SIZE) not in count_per_curr: # go up
                    grid[pe_curr][0][0] = a
                    pos_node_i -= 1
                    change = True
                    #print("top 1")
            
                if not change: # not routing
                    return False
            
            if not change: # not routing
                return False
            
            dist_i, dist_j = abs(pos_b_i - pos_node_i), abs(pos_b_j - pos_node_j)
            dist_walk += 1
            change = False

        if change: # stop, give errors
            return False
        
        pe_final = pos_node_i * GRID_SIZE + pos_node_j
        dic_path[key].append(pe_final)

        # update cost edge
        dic_cost[key] = dist_walk

    return True

def routing_1hop(list_edge, NODE_SIZE, GRID_SIZE, TOTAL_GRID_SIZE, positions, grid, dic_cost, dic_path, dic_pe):

    # verify if is routing
    for j in range(0, len(list_edge), 2):
        a = int(list_edge[j])
        b = int(list_edge[j+1])
        key = list_edge[j] + "_" + list_edge[j+1]
        pos_a_i = positions[str(a)][0]
        pos_a_j = positions[str(a)][1]
        pos_b_i = positions[str(b)][0]
        pos_b_j = positions[str(b)][1]

        dic_pe[a] = pos_a_i * GRID_SIZE + pos_a_j
        dic_pe[b] = pos_b_i * GRID_SIZE + pos_b_j

        dic_path[key] = []
        dist_walk = -1

        diff_i, diff_j = pos_b_i - pos_a_i, pos_b_j - pos_a_j
        dist_i, dist_j = abs(pos_b_i - pos_a_i), abs(pos_b_j - pos_a_j)

        pos_node_i, pos_node_j = pos_a_i, pos_a_j
        change = False
        
        count_per_curr = []
        
        while dist_i != 0 or dist_j != 0:
            diff_i = pos_b_i - pos_node_i
            diff_j = pos_b_j - pos_node_j

            # get the current position node
            pe_curr = pos_node_i * GRID_SIZE + pos_node_j
            dic_path[key].append(pe_curr)
            count_per_curr.append(pe_curr)

            # go to right neighbor
            # [pe], [0 = top, 1 = right, 2 = down, 3 = left], [0 = IN, OUT = 1]
            if diff_j > 0 and dist_j >= 2 and pe_curr+2 < (pos_node_i+1)*GRID_SIZE and (grid[pe_curr][1][1] == -1 or grid[pe_curr][1][1] == a) and grid[pe_curr+2][3][1] != a and (pe_curr+2) not in count_per_curr:  # go right
                grid[pe_curr][1][1] = a
                pos_node_j += 2
                change = True
                #print("VIZ right 2")
            elif diff_j > 0 and pe_curr+1 < (pos_node_i+1)*GRID_SIZE and (grid[pe_curr][1][0] == -1 or grid[pe_curr][1][0] == a) and grid[pe_curr+1][3][0] != a and (pe_curr+1) not in count_per_curr:  # go right
                grid[pe_curr][1][0] = a
                pos_node_j += 1
                change = True
                #print("VIZ right 1")
            elif diff_j < 0 and dist_j >= 2 and pe_curr-2 >= (pos_node_i)*GRID_SIZE and (grid[pe_curr][3][1] == -1 or grid[pe_curr][3][1] == a) and grid[pe_curr-2][1][1] != a and (pe_curr-2) not in count_per_curr: # go left
                grid[pe_curr][3][1] = a
                pos_node_j -= 2
                change = True
                #print("VIZ left 2")
            elif diff_j < 0 and pe_curr-1 >= (pos_node_i)*GRID_SIZE and (grid[pe_curr][3][0] == -1 or grid[pe_curr][3][0] == a) and grid[pe_curr-1][1][0] != a and (pe_curr-1) not in count_per_curr: # go left
                grid[pe_curr][3][0] = a
                pos_node_j -= 1
                change = True
                #print("VIZ left 1")
            elif diff_i > 0 and dist_i >= 2 and pe_curr+2*GRID_SIZE < TOTAL_GRID_SIZE and (grid[pe_curr][2][1] == -1 or grid[pe_curr][2][1] == a) and grid[pe_curr+2*GRID_SIZE][0][1] != a and (pe_curr+2*GRID_SIZE) not in count_per_curr: # go down
                grid[pe_curr][2][1] = a
                pos_node_i += 2
                change = True
                #print("VIZ down 2")
            elif diff_i > 0 and pe_curr+GRID_SIZE < TOTAL_GRID_SIZE and (grid[pe_curr][2][0] == -1 or grid[pe_curr][2][0] == a) and grid[pe_curr+GRID_SIZE][0][0] != a and (pe_curr+GRID_SIZE) not in count_per_curr: # go down
                grid[pe_curr][2][0] = a
                pos_node_i += 1
                change = True
                #print("VIZ down 1")
            elif diff_i < 0 and dist_i >= 2 and pe_curr-2*GRID_SIZE >= 0 and (grid[pe_curr][0][1] == -1 or grid[pe_curr][0][1] == a) and grid[pe_curr-2*GRID_SIZE][2][1] != a and (pe_curr-2*GRID_SIZE) not in count_per_curr: # go up
                grid[pe_curr][0][1] = a
                pos_node_i -= 2
                change = True
                #print("VIZ top 2")
            elif diff_i < 0 and pe_curr-GRID_SIZE >= 0 and (grid[pe_curr][0][0] == -1 or grid[pe_curr][0][0] == a) and grid[pe_curr-GRID_SIZE][2][0] != a and (pe_curr-GRID_SIZE) not in count_per_curr: # go up
                grid[pe_curr][0][0] = a
                pos_node_i -= 1
                change = True
                #print("VIZ top 1")
        
            if not change: # change, try a long path  
                
                if pe_curr+1 < (pos_node_i+1)*GRID_SIZE and (grid[pe_curr][1][0] == -1 or grid[pe_curr][1][0] == a) and grid[pe_curr+1][3][0] != a and (pe_curr+1) not in count_per_curr:  # go right
                    grid[pe_curr][1][0] = a
                    pos_node_j += 1
                    change = True
                    #print("right 1")
                elif pe_curr-1 >= (pos_node_i)*GRID_SIZE and (grid[pe_curr][3][0] == -1 or grid[pe_curr][3][0] == a) and grid[pe_curr-1][1][0] != a and (pe_curr-1) not in count_per_curr: # go left
                    grid[pe_curr][3][0] = a
                    pos_node_j -= 1
                    change = True
                    #print("left 1")
                elif pe_curr+GRID_SIZE < TOTAL_GRID_SIZE and (grid[pe_curr][2][0] == -1 or grid[pe_curr][2][0] == a) and grid[pe_curr+GRID_SIZE][0][0] != a and (pe_curr+GRID_SIZE) not in count_per_curr: # go down
                    grid[pe_curr][2][0] = a
                    pos_node_i += 1
                    change = True
                    #print("down 1")
                elif pe_curr-GRID_SIZE >= 0 and (grid[pe_curr][0][0] == -1 or grid[pe_curr][0][0] == a) and grid[pe_curr-GRID_SIZE][2][0] != a and (pe_curr-GRID_SIZE) not in count_per_curr: # go up
                    grid[pe_curr][0][0] = a
                    pos_node_i -= 1
                    change = True
                    #print("top 1")
            
                if not change: # not routing
                    return False
            
            if not change: # not routing
                return False
            
            dist_i, dist_j = abs(pos_b_i - pos_node_i), abs(pos_b_j - pos_node_j)
            dist_walk += 1
            change = False

        if change: # stop, give errors
            return False
        
        pe_final = pos_node_i * GRID_SIZE + pos_node_j
        dic_path[key].append(pe_final)

        # update cost edge
        dic_cost[key] = dist_walk

    return True