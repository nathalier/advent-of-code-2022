from itertools import pairwise
from copy import copy
from collections import deque


def flow_sand(filled, start_point, bottom_level):
    def enclosing(position):
        return [position, position - 1, position + 1]

    def potential_sources(point):
        return [(i, point[1] - 1) for i in enclosing(point[0])]

    def potential_sinks(point):
        return [(i, point[1] + 1) for i in enclosing(point[0])]

    def sinks(point):
        return [sink for sink in potential_sinks(point)
                if (sink not in filled) and (bottom_level is None or sink[1] < bottom_level)]

    def land_here(point):
        filled.add(point)
        for source in potential_sources(point):
            if source in possible_ways:
                possible_ways[source].remove(point)

    def sand_flow():
        while not (path_to_void_found or start_point in filled):
            yield start_point

    
    possible_ways = {}
    landed_count = 0
    path_to_void_found = False

    for next_portion_pos in sand_flow():
        cur_portion_pos = next_portion_pos
        while True:
            if cur_portion_pos not in possible_ways:
                possible_ways[cur_portion_pos] = deque(sinks(cur_portion_pos))

            if len(possible_ways[cur_portion_pos]) == 0:
                land_here(cur_portion_pos)
                landed_count += 1
                break

            cur_portion_pos = possible_ways[cur_portion_pos][0]

            if bottom_level is None and cur_portion_pos[1] >= lowest_wall:
                path_to_void_found = True  
                break             
    return landed_count


def part_1(filled, start_point):
    return flow_sand(filled, start_point, bottom_level=None)


def part_2(filled, start_point):
    bottom_level = lowest_wall + 2
    return flow_sand(filled, start_point, bottom_level)


def read_data(filename):
    filled = set()
    lowest_wall = -1
    with open(filename) as f:
        for path in f:
            corners = list(map(lambda point: tuple(map(int, point.split(','))), path.strip().split(' -> ')))
            lowest_wall = max([lowest_wall, max([x[1] for x in corners])])
            for start, end in pairwise(corners):
                filled.update([(i, j) 
                        for i in range(min(start[0], end[0]), max(start[0], end[0]) + 1)
                        for j in range(min(start[1], end[1]), max(start[1], end[1]) + 1)])
    return filled, lowest_wall


#############################
start_point = (500, 0)
filled, lowest_wall = read_data('input_t.txt')

assert (res := part_1(copy(filled), start_point)) == 24, f'Actual: {res}'
assert (res := part_2(copy(filled), start_point)) == 93, f'Actual: {res}'
#############################

filled, lowest_wall = read_data('input.txt')

print(part_1(copy(filled), start_point))
print(part_2(copy(filled), start_point))
