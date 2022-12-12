from string import ascii_lowercase
from copy import copy
from collections import defaultdict


def shortest_path(topo_map, start, destination, max_alt_gain=1, cache=None):
    def fill_path_from_cache(cell, prev_cell):
            best_distances[destination] = best_distances[cell] + cache[cell]['dist']
            prev_opt_path_cell = prev_cell
            for i, opt_path_cell in enumerate(cache[cell]["path"]):
                best_distances[opt_path_cell] = best_distances[cell] + i
                came_from[opt_path_cell] = prev_opt_path_cell
                if opt_path_cell not in unvisited:
                    break
                if opt_path_cell != destination:
                    unvisited.remove(opt_path_cell)
                prev_opt_path_cell = opt_path_cell

    def get_next_unvisited():
        unvisited_dist = {key: best_distances[key] for key in best_distances if key in unvisited}
        return min(unvisited_dist, key=unvisited_dist.get)

    def update_cache():
        path = build_path(destination, came_from)
        for i, cell in enumerate(path):
            cache[cell]["dist"] = best_distances[destination] - i
            cache[cell]["path"] = copy(path[i:])
        if not path:
            for cell in [key for key in best_distances if best_distances[key] < float('inf')]:
                cache[cell]["dist"] = float('inf')
                cache[cell]["path"] = []


    cache = defaultdict(dict) if cache is None else cache
    if start in cache:
        return cache[start]['dist']

    rows_num, cols_num = len(topo_map), len(topo_map[0])

    unvisited = set([(i, j) for i in range(rows_num) for j in range(cols_num)])
    best_distances = {(i, j): float('inf') for i in range(rows_num) for j in range(cols_num)}
    came_from = {}

    cur_cell, cur_best_dist = start, 0
    came_from[cur_cell] = cur_cell
    best_distances[cur_cell] = cur_best_dist

    while cur_cell != destination and cur_cell is not None:
        reachable_neighbours = get_reachable(cur_cell, topo_map, max_alt_gain)
        for cell in reachable_neighbours:
            if best_distances[cell] > cur_best_dist + 1:
                best_distances[cell] = cur_best_dist + 1
                came_from[cell] = cur_cell
                if cell in cache and \
                        best_distances[destination] > \
                        best_distances[cell] + cache[cell]['dist']:
                    fill_path_from_cache(cell, cur_cell)
        unvisited.remove(cur_cell)
        cur_cell = get_next_unvisited()
        cur_best_dist = best_distances[cur_cell]
        
    update_cache()
    
    return best_distances[destination]
        
        
def build_path(cell, came_from):
    if cell not in came_from:
        return []

    cur_cell = cell
    path = [cur_cell]
    while came_from[cur_cell] != cur_cell:
        cur_cell = came_from[cur_cell]
        path.append(cur_cell)
    return list(reversed(path))


def get_reachable(cell, topo_map, max_alt_gain):
    rows_num, cols_num = len(topo_map), len(topo_map[0])
    neighbours = get_neighbours(cell, rows_num, cols_num)
    reachable = list(filter(
            lambda ne: topo_map[ne[0]][ne[1]] - topo_map[cell[0]][cell[1]] <= max_alt_gain,
            neighbours))
    return reachable


def get_neighbours(cell, rows_num, cols_num):
    potential_neighbours = [(cell[0] - 1, cell[1]), 
                            (cell[0] + 1, cell[1]), 
                            (cell[0], cell[1] - 1), 
                            (cell[0], cell[1] + 1)]
    return list(filter(
        lambda cell: 0 <= cell[0] < rows_num and 0 <= cell[1] < cols_num, 
        potential_neighbours))


def part_1(topo_map, start, destination):
    return shortest_path(topo_map, start, destination)


def part_2(topo_map, end):
    cache = defaultdict(dict)
    best_path_len = float('inf')

    potential_starts = set([(i, j) 
                        for i in range(len(topo_map)) 
                        for j in range(len(topo_map[0])) 
                        if topo_map[i][j] == 0])

    best_path_len = min([shortest_path(topo_map, start, end, cache=cache)
                                    for start in potential_starts ])

    return best_path_len


def read_data(filename):
    topo_map = []
    cur_line = 0
    with open(filename) as f:
        for line in f:
            if 'S' in line:
                start_pos = (cur_line, line.find('S'))
            if 'E' in line:
                dest_pos = (cur_line, line.find('E'))
            topo_map.append([map_levels_tr_t[c] for c in line.strip()])
            cur_line += 1
    return topo_map, start_pos, dest_pos


map_levels_tr_t = dict(zip(ascii_lowercase, range(26))) | {'S': 0, 'E': 25}

#############################
topo_map, start_pos, dest_pos = read_data('input_t.txt')

assert part_1(topo_map, start_pos, dest_pos) == 31
assert part_2(topo_map, dest_pos) == 29
#############################


topo_map, start_pos, dest_pos = read_data('input.txt')

print(part_1(topo_map, start_pos, dest_pos))
print(part_2(topo_map, dest_pos))
