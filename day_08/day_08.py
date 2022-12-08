import numpy as np
from functools import reduce
from operator import mul


def part_1(data):
    vissible_num = (data.shape[0] + data.shape[1] - 2) * 2

    for i in range(1, data.shape[0] - 1):
        for j in range(1, data.shape[1] - 1):
            tree_lines = [data[0:i, j], data[i+1:, j], data[i, 0:j], data[i, j+1:]]
            vissible_num += any(list(map(np.max, tree_lines)) < data[i,j])
    
    return vissible_num


def part_2(data):
    scenic_score = 0

    for i in range(1, data.shape[0] - 1):
        for j in range(1, data.shape[1] - 1):
            tree_lines = [data[i-1::-1, j], data[i+1:, j], data[i, j-1::-1], data[i, j+1:]]
            lines_score = map(lambda line: get_line_scenic_score(line, data[i, j]), tree_lines)
            scenic_score = max(scenic_score, reduce(mul, lines_score, 1))
    
    return scenic_score


def get_line_scenic_score(line, blocking_h):
    return len(line) if max(line) < blocking_h else np.argmax(line >= blocking_h) + 1


def read_data(filename):
    with open(filename) as f:
        data = np.array(list(map(lambda x: list(map(int, list(x.strip()))), f.readlines())))
    return data


#############################
test_data = read_data('input_t.txt')

assert part_1(test_data) == 21
assert part_2(test_data) == 8
#############################


data = read_data('input.txt')

print(part_1(data))
print(part_2(data))
