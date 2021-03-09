import networkx as nx

def operation(g, node, dic_pe, dic_opcode, dic_value, dic_port, dict_dit, buffer, path, arq):
    list_son = list(g.predecessors(node))
    array = [""] * len(list_son)

    #print(list_son)
    #print(dic_opcode)
    
    for son in list_son:
        key = str()
        edge = int(dic_port[(son,node)])
        if node == son:
            array[edge] = "$acc"
        elif dic_opcode[son] == "const":
            array[edge] = dic_value[son]
        else:
            key = str(dict_dit[son]) + "_" + str(dict_dit[node])
            array[edge] = ""
            if int(buffer[key]) > 0:
                array[edge] += "#" + buffer[key] + " "
            array[edge] += "$" + str(path[key][-2])
    
    arq.write("%s $%s" %(dic_opcode[node], dic_pe[node]))
    print("%s $%s" %(dic_opcode[node], dic_pe[node]), end="")
    for i in range(len(array)):
        arq.write(" " + array[i])
        print(" " + array[i], end="")
    arq.write("\n")
    print()


def cgra_assembly(g, buffer, path, edges, dict_inv, dict_dir, GRID_SIZE, pe, name):

    dic_opcode = nx.get_node_attributes(g, 'opcode')
    dic_value = nx.get_node_attributes(g, 'value')
    dic_port = nx.get_edge_attributes(g, 'port')
    
    #print(dic_opcode)
    #print(dic_value)
    #print(dic_port)
    #print(pe)
    #print(dict_inv)
    print(path)

    dic_pe = {}
    for elem in pe:
        dic_pe[dict_inv[str(elem)]] = str(pe[elem])
    
    arq = open("cgra/"+name+".asm", "w")

    print("map\n")
    for n in g.nodes():
        op = dic_opcode[n]
        #print("----->", n)
        if op == "const":
            continue # ignore the node
        elif op in ["load", "input", "istream"]:
            arq.write("pass $%s $istream\n" %dic_pe[n])
        elif op in ["store", "output", "ostream"]:
            son = list(g.predecessors(n))[0]
            key = str(dict_dir[son]) + "_" + str(dict_dir[n])
            arq.write("pass $%s $%s\n" %(dic_pe[n], path[key][-2]))
        elif op in ["add", "mul"]:
            operation(g, n, dic_pe, dic_opcode, dic_value, dic_port, dict_dir, buffer, path, arq)

    print("\nroute\n")
    for e in g.edges():
        op1 = dic_opcode[e[0]]
        op2 = dic_opcode[e[1]]
        if op1 == "const" or op2 == "const":
            continue # ver com o lucas
        elif e[0] == e[1]:
            continue
        
        key = str(dict_dir[e[0]]) + "_" + str(dict_dir[e[1]])
        #print("---->", key)

        for i in range(0, len(path[key])-1):
            if i == 0:
                print("route $%s $alu $%s" %(str(path[key][i]), str(path[key][i+1])))
                arq.write("route $%s $alu $%s\n" %(str(path[key][i]), str(path[key][i+1]))) 
            else:
                print("route $%s $%s $%s" %(str(path[key][i]), str(path[key][0]), str(path[key][i+1])))
                arq.write("route $%s $%s $%s\n" %(str(path[key][i]), str(path[key][0]), str(path[key][i+1]))) 
        if op2 in ["store", "output", "stream"]:
            print("route $%s $alu $ostream" %(str(path[key][-1])))
            arq.write("route $%s $alu $ostream\n" %(str(path[key][-1])))
    arq.close()