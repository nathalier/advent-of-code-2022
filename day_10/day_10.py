from itertools import tee


def part_1(data_gen, main_cycle_gen):
    cycle, x, main_sygnals_acc = 1, 1, 0
    main_cycle = next(main_cycle_gen)

    for signal in data_gen:
        if cycle == main_cycle:
            main_sygnals_acc += cycle * x
            main_cycle = next(main_cycle_gen)
        cycle += 1
        x += signal

    return main_sygnals_acc


def part_2(data_gen, row_len=40):
    cycle, x = 0, 1
    rows = [] 

    for signal in data_gen:
        stripe_pos = (x-1, x, x+1)
        draw_col = cycle % row_len
        if draw_col == 0:
            rows.append([])
        rows[-1].append('#' if draw_col in stripe_pos else ' ')
        cycle += 1
        x += signal

    for row in rows:
        print(''.join(row))


def data_generator(filename):
    with open(filename) as f:
        while next_line := f.readline().strip():
            instr = list(map(try_int, next_line.split()))
            match instr[0]:
                case 'noop':
                    yield 0
                case 'addx':
                    yield 0
                    yield instr[1]


def try_int(item):
    try:
        return int(item)
    except ValueError:
        return item


def main_cycle_gen(start_val, step):
    val = start_val
    while True:
        yield start_val
        start_val += step



#############################
test_data_base_gen = data_generator('input_t.txt')
test_data_gens = tee(test_data_base_gen, 2)

assert part_1(test_data_gens[0], main_cycle_gen(20, 40)) == 13140
part_2(test_data_gens[1])
#############################


data_base_gen = data_generator('input.txt')
data_gens = tee(data_base_gen, 2)

print(part_1(data_gens[0], main_cycle_gen(20, 40)))
part_2(data_gens[1])
