from utils import get_id


def create_neighbors(shape, i, j, arch_type):
    L, C = shape
    neighbors = []

    if i > 0:
        neighbors.append(get_id(i - 1, j, C))
    if j > 0:
        neighbors.append(get_id(i, j - 1, C))
    if i < L - 1:
        neighbors.append(get_id(i + 1, j, C))
    if j < C - 1:
        neighbors.append(get_id(i, j + 1, C))

    if arch_type == 'one-hop':
        if i > 1:
            neighbors.append(get_id(i - 2, j, C))
        if j > 1:
            neighbors.append(get_id(i, j - 2, C))
        if i < L - 2:
            neighbors.append(get_id(i + 2, j, C))
        if j < C - 2:
            neighbors.append(get_id(i, j + 2, C))
    elif arch_type == 'chess':
        if get_id(i, j, C) % 2 != 0:
            if i > 1:
                neighbors.append(get_id(i - 2, j, C))
            if j > 1:
                neighbors.append(get_id(i, j - 2, C))
            if i < L - 2:
                neighbors.append(get_id(i + 2, j, C))
            if j < C - 2:
                neighbors.append(get_id(i, j + 2, C))
    elif arch_type == 'diagonal':
        if i > 0 and j > 0:
            neighbors.append(get_id(i - 1, j - 1, C))
        if i > 0 and j < C - 1:
            neighbors.append(get_id(i - 1, j + 1, C))
        if i < L - 1 and j > 0:
            neighbors.append(get_id(i + 1, j - 1, C))
        if i < L - 1 and j < C - 1:
            neighbors.append(get_id(i + 1, j + 1, C))
    elif arch_type == 'hexagonal':
        neighbors = []
        if j > 0:
            neighbors.append(get_id(i, j - 1, C))
        if j < C - 1:
            neighbors.append(get_id(i, j + 1, C))

        if i % 2 == 0:
            if i < L - 1:
                neighbors.append(get_id(i + 1, j, C))
            if i > 0:
                neighbors.append(get_id(i - 1, j, C))
            if i < L - 1 and j < C - 1:
                neighbors.append(get_id(i + 1, j + 1, C))
            if i > 0 and j < C - 1:
                neighbors.append(get_id(i - 1, j + 1, C))
        else:
            if i > 0 and j > 0:
                neighbors.append(get_id(i - 1, j - 1, C))
            if i > 0:
                neighbors.append(get_id(i - 1, j, C))
            if i < L - 1 and j > 0:
                neighbors.append(get_id(i + 1, j - 1, C))
            if i < L - 1:
                neighbors.append(get_id(i + 1, j, C))

    return neighbors


def create_cgra(arch_net, shape, isa, routes, fifos, acc, data_width, conf_bus_width):
    json_arch = {'shape': list(shape), 'data_width': data_width, 'conf_bus_width': conf_bus_width,
                 'pe': []}

    for i in range(shape[0]):
        for j in range(shape[1]):
            id = get_id(i, j, shape[1])
            if j == 0:
                pe_type = 'input'
            elif j == shape[1] - 1:
                pe_type = 'output'
            else:
                pe_type = 'basic'

            neighbors = create_neighbors(shape, i, j, arch_net)
            pe = {'id': id, 'type': pe_type, 'neighbors': neighbors, 'routes': routes, 'elastic_queue': fifos,
                  'acc': acc, 'isa': isa}
            json_arch['pe'].append(pe)

    return json_arch
