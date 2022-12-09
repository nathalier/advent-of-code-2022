from copy import copy
import numpy as np


def trace_tail(moves, knots_num):
    knot_positions = [np.array([0, 0])] * (knots_num + 1)
    tail_visited = set()
    tail_visited.add((0, 0))

    for direction, steps in moves:
        for _ in range(steps):
            knot_positions[0] = knot_positions[0] + 1 * direction
            for i in range(len(knot_positions) - 1):
                tail_pos, newly_visited = adjust_tail(knot_positions[i], knot_positions[i+1]) 
                knot_positions[i+1] = tail_pos
                if not newly_visited:
                    break
            tail_visited.update(newly_visited)
    
    return len(tail_visited)


def adjust_tail(head_pos, tail_pos):
    tail_visited = []

    while any(np.abs(head_pos - tail_pos) > 1):
        step_direction = np.sign(head_pos - tail_pos)
        tail_pos = tail_pos + step_direction
        tail_visited.append(tuple(tail_pos.tolist()))

    return tail_pos, tail_visited


def part_1(data):
    # return trace_tail(data, 1)  # less optimal

    head_pos, tail_pos = np.array([0, 0]), np.array([0, 0])
    tail_visited = set()
    tail_visited.add(((0, 0)))

    for move in data:
        head_move_vector = np.array(move[0]) * move[1]
        head_pos = head_pos + head_move_vector
        tail_pos, newly_visited = adjust_tail(head_pos, tail_pos) 
        tail_visited.update(newly_visited)

    return len(tail_visited)


def part_2(data):
    return trace_tail(data, 9)


def read_data(filename):
    def decode_line(line):
        instr = line.strip().split()
        instr[0] = move_directions[instr[0]]
        instr[1] = int(instr[1])
        return instr

    move_directions = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1), 
    }

    with open(filename) as f:
        data = list(map(decode_line, f.readlines()))
    return data


#############################
test_data = read_data('input_t.txt')

assert part_1(test_data) == 13
assert part_2(test_data) == 1

test_data_2 = read_data('input_t_2.txt')
assert part_2(test_data_2) == 36
#############################


data = read_data('input.txt')

print(part_1(data))
print(part_2(data))
