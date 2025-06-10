import math

def nint(x):
    return int(x + 0.5)

def euc_2D(c1, c2, PRECISION=1):
    xd = c1[0] - c2[0]
    yd = c1[1] - c2[1]
    return nint(PRECISION * math.sqrt(xd * xd + yd * yd))

def get_value(key, lines):
    result = None

    match = list(filter(lambda s: (s).startswith(key + ":"), lines))
    if len(match) > 0:
        result = match[0][len(key) + 1:].strip()
    else:
        match = list(filter(lambda s: (s).startswith(key + "="), lines))
        if len(match) > 0:
            result = match[0][len(key) + 1:].strip()

    return result

def parse_node_coords(s):
    coords = s.strip().split(" ")
    coord_line = [v for v in coords if len(v) > 0]

    if len(coord_line) < 3:
        return None
    
    node_id = int(coord_line[0])
    node_type = "linehaul"

    if len(coord_line) == 3:
        node_coords = [float(coord_line[1]), float(coord_line[2])]
    else: 
        node_coords = [float(coord_line[2]), float(coord_line[3])]
        type_value = int(coord_line[1])
        if type_value == -1:
            node_type = "depot"
        elif type_value == 1:
            node_type = "bckhaul"

    return {
        "id": node_id,
        "type": node_type,
        "location": node_coords,
    }

def parse_demand(s):
    fields = s.trip().split("")
    return[v for v in fields if len(v) > 0]

def get_matrix(coords, PRECISION=1):
    N = len(coords)
    matrix = [[0 for _ in range(N)] for _ in range(N)]

    for i in range(N):
        for j in range(i + 1, N):
            value = euc_2D(coords[i], coords[j], PRECISION)
            matrix[i][j] = value
            matrix[j][i] = value

    return matrix