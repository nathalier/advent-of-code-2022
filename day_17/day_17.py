from itertools import cycle, islice
import numpy as np


def part_1(air_flow_pat, rocks_num):
    height= 0
    terrain = np.ones((1, width), dtype='bool')
    rocks = next_rock()
    air_flow = airflow(air_flow_pat)
    for i in range(rocks_num):
        terrain, _ = fall(next(rocks), air_flow, terrain, rock_fill=True)
        height = max_height(terrain)
    return height


def digit():
    source = cycle(range(1, 6))
    for d in source:
        yield d


def part_2(air_flow_pat, rocks_num, jet_pat_len):
    height, acc_h = 0, 0
    terrain = np.ones((1, width), dtype='int')
    digits = digit()
    rocks = next_rock()
    air_flow = airflow(air_flow_pat)
    patterns = []
    first_occ, last_occ = 0, 0
    magic_constant = 2000

    i = 0
    while i < rocks_num:
        i += 1
        rock_fill = next(digits)
        terrain, last_jet_idx = fall(next(rocks), air_flow, terrain, rock_fill)

        if (not first_occ) and (i % (magic_constant) == 0):
            terrain, acc_h = cut_base(terrain, acc_h)
            height = max_height(terrain)
            print(f'idx: {i // (magic_constant) - 1}, {i = }, {height = }, {acc_h = }, {last_jet_idx = }')
            pattern, pat_step = terrain[:height+1], i
            for idx, prev_pat in enumerate(patterns[:100]):
                if np.array_equal(prev_pat[0], pattern) and last_jet_idx == prev_pat[3]:
                    print(f'Found! {prev_pat[1]} == {pat_step}')
                    first_occ, last_occ, prev_acc_h, base_cycle_idx = prev_pat[1], pat_step, prev_pat[2], idx
                    break
            patterns.append((pattern, pat_step, acc_h, last_jet_idx))
            if first_occ:
                k = (rocks_num - first_occ) // (last_occ - first_occ)
                i = (last_occ - first_occ) * k + first_occ
                print(f'{k = }, {i = }, {acc_h = }, {prev_acc_h = }, {base_cycle_idx = }')
                acc_h += (acc_h - prev_acc_h) * (k - 1)
                # print_terrain(pattern)

                additional_cycles = (rocks_num - i) // (magic_constant)
                if additional_cycles:
                    cache_idx = base_cycle_idx + additional_cycles
                    i += additional_cycles * magic_constant
                    print(cache_idx)
                    print(f'{additional_cycles = }, {cache_idx = }, {patterns[cache_idx][2] = }, {prev_acc_h = }, {i = }')
                    acc_h += (patterns[cache_idx][2] - patterns[base_cycle_idx][2])
                    terrain = patterns[cache_idx][0]
                    jet_idx = patterns[cache_idx][3]
                
                air_flow = airflow(air_flow_pat)
                print(last_jet_idx)
                air_flow = islice(air_flow, jet_idx + 1, None)

        height = max_height(terrain) 
    
    print(acc_h, height)
    print_terrain(terrain)
    print(f'{i=}')
    return acc_h + height


def print_terrain(terrain):
    print()
    for i in range(terrain.shape[0]-1, -1, -1):
        print(terrain[i])


def fall(rock, jet, terrain, rock_fill):
    tower_h = max_height(terrain)
    terrain = np.r_[terrain, np.zeros((max(0, 4 - (terrain.shape[0] - tower_h - 1)), terrain.shape[1]), dtype='int')]
    l_hor_pos = 2
    r_hor_pos = l_hor_pos + rock.shape[1] - 1
    u_vert_pos = tower_h + 1
    b_vert_pos = u_vert_pos + rock.shape[0] - 1
    pos = (l_hor_pos, r_hor_pos, u_vert_pos, b_vert_pos)
    air_flows = 0

    for _ in range(3):
        pos = try_side_move(terrain, pos, rock, next(jet)[0])
        air_flows += 1
    while True:
        last_jet_flow, last_pat_idx = next(jet)
        pos = try_side_move(terrain, pos, rock, last_jet_flow[0])
        air_flows += 1
        terrain, pos = try_down_move(terrain, pos, rock, rock_fill)
        if pos is None:
            break
    
    return terrain, last_pat_idx


def try_side_move(terrain, pos, rock, direction):
    new_pos = pos
    if direction == '<':
        if pos[0] > 0:
            new_pos = [pos[0]-1, pos[1]-1, pos[2], pos[3]]
    elif direction == '>':
        if pos[1] < terrain.shape[1] - 1:
            new_pos = [pos[0]+1, pos[1]+1, pos[2], pos[3]]
    
    if any(terrain[new_pos[2] : new_pos[3] + 1, new_pos[0] : new_pos[1] + 1][rock]):
        return pos
    return new_pos


def try_down_move(terrain, pos, rock, rock_fill):
    new_pos = [pos[0], pos[1], pos[2]-1, pos[3]-1]

    if any(terrain[new_pos[2] : new_pos[3] + 1, new_pos[0] : new_pos[1] + 1][rock] > 0):
        terrain[pos[2] : pos[3] + 1, pos[0] : pos[1] + 1][rock] = rock_fill
        return terrain, None
    return terrain, new_pos


def cut_base(terrain, acc):
    base_h = blocked_h(terrain)
    terrain = terrain[base_h:]
    acc += base_h
    return terrain, acc


def max_height(terrain):
    for row_num in range(terrain.shape[0]-1, -1, -1):
        if any(terrain[row_num] > 0):
            return row_num


def blocked_h(terrain):
    blocked_height = terrain.shape[0]
    for col_num in range(terrain.shape[1]):
        for row_num in range(terrain.shape[0]-1, -1, -1):
            if terrain[row_num][col_num] > 0:
                blocked_height = min(blocked_height, row_num)
                break
    return blocked_height


def next_rock():
    while True:
        yield np.array([[True, True, True, True]])
        yield np.array([[False, True, False], [True, True, True], [False, True, False]])
        yield np.array([[True, True, True], [False, False, True], [False, False, True]])
        yield np.array([[True], [True], [True], [True]])
        yield np.array([[True, True], [True, True]])

def airflow(pattern):
    endless_p = zip(cycle(pattern), cycle(range(len(pattern))))
    while True:
        yield next(endless_p)


def read_data(filename):
    with open(filename) as f:
        data = f.read().strip()
        print(f'{len(data) = }')
    return data


#############################
jet_pattern = read_data('input_t.txt')
width = 7
kinds_of_blocks = 5

assert (res := part_1(jet_pattern, rocks_num=2022)) == 3068, f'Actual: {res}'
assert (res := part_2(jet_pattern, rocks_num=1_000_000_000_000, jet_pat_len=len(jet_pattern))) == 1514285714288, f'Actual: {res}'
#############################


jet_pattern_m = read_data('input.txt')

print(part_1(jet_pattern_m, rocks_num=2022))
print(part_2(jet_pattern_m, rocks_num=1_000_000_000_000, jet_pat_len=len(jet_pattern_m)))

# Found! 100910 == 5297775
# 192423 999996454805 8157600 155345
# 1539823528213 9
# 1539823528222

# Found! 100910 == 5297775
# k = 192423, i = 999996454805, acc_h = 8157600, prev_acc_h = 155345, prev_cycle_idx = 1
# additional_cycles = 70, cache_idx = 71, acc_h = 1539818069210, prev_acc_h = 155345, i = 999999986655
# 1539823528184 11
# 1539823528195

# 1539823683586
# 1539815681331

# print(5769721 + 192423 * (8157600 - 155345))


# <>><>>><<<>>><<<><<<>><>><<>>>>><<><>><<<>><>>><<<>>><
# <>><<<>><>>><<<>>><<<><<<>><>><<>>>>><<><>><<<>><>>><
