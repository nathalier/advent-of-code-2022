from string import ascii_lowercase
import networkx as nx
from itertools import repeat
from collections import deque
from timeit import timeit


def shortest_path(topo_graph, start, destinations):
    def get_next_unvisited():
        unvisited_dist = {key: best_distances[key] for key in best_distances if key in unvisited}
        return min(unvisited_dist, key=unvisited_dist.get, default=None)
    
    if isinstance(destinations, tuple):
        destinations = [destinations]

    unvisited = set(topo_graph.nodes)
    unvisited_destinations = set(destinations)
    best_distances = {node: float('inf') for node in topo_graph.nodes}

    cur_node = start
    best_distances[cur_node] = 0

    while unvisited_destinations and cur_node is not None:
        cur_best_dist = best_distances[cur_node]
        successors = topo_graph.successors(cur_node)
        for node in successors:
            if best_distances[node] > cur_best_dist + 1:
                best_distances[node] = cur_best_dist + 1
        unvisited.remove(cur_node)
        unvisited_destinations.discard(cur_node)
        cur_node = get_next_unvisited()
                
    return min([best_distances[dest] for dest in destinations])


def bfs(topo_graph, start, destinations):

    if isinstance(destinations, tuple):
        destinations = [destinations]

    unvisited_nodes = set(topo_graph.nodes)
    distances_to = {node: float('inf') for node in topo_graph.nodes}

    cur_dist = 0
    nodes_que = deque([(start, cur_dist)])

    while nodes_que:
        cur_node = nodes_que.popleft()
        if cur_node[0] in destinations:
            return cur_node[1]
        if cur_node[0] in unvisited_nodes:
            cur_dist = cur_node[1]
            distances_to[cur_node[0]] = cur_dist
            for node in topo_graph.successors(cur_node[0]):
                if node in unvisited_nodes:
                    nodes_que.append((node, cur_dist + 1))
            unvisited_nodes.discard(cur_node[0])
    
    return None


def part_1_dijkstra(topo_graph, start, destination):
    return shortest_path(topo_graph, start, destination)
    

def part_1_bfs(topo_graph, start, destination):
    return bfs(topo_graph, start, destination)


def part_2_dijkstra(topo_graph, destination):
    starts = [node[0] for node in topo_graph.nodes(data=True) if node[1]['value'] == 0]
    reversed_topo_graph = topo_graph.reverse()
    return shortest_path(reversed_topo_graph, destination, starts)


def part_2_bfs(topo_graph, destination):
    starts = [node[0] for node in topo_graph.nodes(data=True) if node[1]['value'] == 0]
    reversed_topo_graph = topo_graph.reverse()
    return bfs(reversed_topo_graph, destination, starts)


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


def build_graph(topo_map):
    G = nx.DiGraph()
    G.add_nodes_from([((i, j), {'value': topo_map[i][j]}) for i in range(len(topo_map)) for j in range(len(topo_map[0]))])
    for i in range(len(topo_map)):
        for j in range(len(topo_map[0])):
            reachable = get_reachable((i,j), topo_map, max_alt_gain=1)
            G.add_edges_from(list(zip(repeat((i, j)), reachable)))
    return G


map_levels_tr_t = dict(zip(ascii_lowercase, range(26))) | {'S': 0, 'E': 25}

#############################
topo_map, start_pos, dest_pos = read_data('input_t.txt')
topo_graph = build_graph(topo_map)

assert part_1_bfs(topo_graph, start_pos, dest_pos) == 31
assert part_2_bfs(topo_graph, dest_pos) == 29
# #############################

print('part_1_dijkstra test data: ', timeit('part_1_dijkstra(topo_graph, start_pos, dest_pos)', number=1000, globals=globals()))
print('part_1_bfs test data: ', timeit('part_1_bfs(topo_graph, start_pos, dest_pos)', number=1000, globals=globals()))
print('part_2_dijkstra test data: ', timeit('part_2_dijkstra(topo_graph, dest_pos)', number=1000, globals=globals()))
print('part_2_bfs test data: ', timeit('part_2_bfs(topo_graph, dest_pos)', number=1000, globals=globals()))

topo_map, start_pos, dest_pos = read_data('input.txt')
topo_graph = build_graph(topo_map)

print(part_1_bfs(topo_graph, start_pos, dest_pos))
print(part_2_bfs(topo_graph, dest_pos))

print('part_1_dijkstra: ', timeit('part_1_dijkstra(topo_graph, start_pos, dest_pos)', number=10, globals=globals()))
print('part_1_bfs: ', timeit('part_1_bfs(topo_graph, start_pos, dest_pos)', number=10, globals=globals()))
print('part_2_dijkstra: ', timeit('part_2_dijkstra(topo_graph, dest_pos)', number=10, globals=globals()))
print('part_2_bfs: ', timeit('part_2_bfs(topo_graph, dest_pos)', number=10, globals=globals()))


# part_1_dijkstra test data:  0.26143239999873913
# part_1_bfs test data:  0.07746580000093672
# part_2_dijkstra test data:  0.7818436999987171
# part_2_bfs test data:  0.5086516000010306
# 361
# 354
# part_1_dijkstra:  20.485329499999352
# part_1_bfs:  0.0855779999983497
# part_2_dijkstra:  21.611355699998967
# part_2_bfs:  1.5214402999990853