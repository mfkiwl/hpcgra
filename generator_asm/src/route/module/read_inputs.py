'''
    Read list and return number of node, edges and order the list
'''
def read_list(dot_list):

    arq = open(dot_list, "r")

    count = 0
    for line in arq:
        line = line.replace("\n", "").split(" ")
        if count == 0:
            n_node = int(line[0])
            n_edge = int(line[1])
        elif count == 2:
            res = []
            for i in range(len(line)):
                if line[i] != '':
                    res.append(line[i])
            edges = res.copy()
        count += 1
    arq.close()
    return n_node, n_edge, edges 

'''
    Read results and return them
'''
def read_results(result):

    arq = open(result, "r")
    vector = []

    count = 0
    for line in arq:
        line = line.replace("\n","").split(" ")
        res = []
        for i in range(len(line)):
            if line[i] != '':
                res.append(line[i])
        vector.append(res)
        count += 1
    arq.close
    return vector

def read_results_vpr(result):

    arq = open(result, "r")
    vector = []

    count = 0
    for line in arq:
        if count == 0:
            dim = int(line)
        else:
            line = line.replace("\n","").split(" ")
            res = []
            for i in range(len(line)):
                if line[i] != '':
                    res.append(line[i])
            vector.append(res)
        count += 1
    arq.close
    return dim, vector