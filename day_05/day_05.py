from collections import namedtuple
import re
from copy import deepcopy


def part_1(stacks, instructions):
    stacks_c = deepcopy(stacks)

    for instr in instructions:
        for i in range(instr.quantity):
            stacks_c[instr.to - 1].append(stacks_c[instr.frm - 1].pop())
    return ''.join([st[-1] or ' ' for st in stacks_c])


def part_2(stacks, instructions):
    stacks_c = deepcopy(stacks)
    
    for instr in instructions:
        stacks_c[instr.to - 1].extend(stacks_c[instr.frm - 1][-instr.quantity:])
        del stacks_c[instr.frm - 1][-instr.quantity:]
    return ''.join([st[-1] or ' ' for st in stacks_c])


def read_data(filename):
    with open(filename) as f:
        data = list(map(lambda x: x.strip('\n'), f.readlines()))

    read_stacks = True
    levels, instructions = [], []
    Instr = namedtuple('Instr', 'quantity frm to')
    for line in data:
        if not line:
            read_stacks = False
            continue
        if read_stacks:
            levels.append([line[i] for i in range(1, len(line), 4)])
        else:
            matcher = re.match('^.*?(\d+).*?(\d+).*?(\d+)$', line)
            next_instr = Instr(*list(map(int, matcher.groups())))
            instructions.append(next_instr)

    stacks = [list(''.join([levels[j][i] for j in range(len(levels)-2, -1, -1)]).strip()) 
                    for i in range(len(levels[-1]))]
        
    return stacks, instructions


#############################
test_stacks, test_instructions = read_data('input_t.txt')

assert part_1(test_stacks, test_instructions) == 'CMZ'
assert part_2(test_stacks, test_instructions) == 'MCD'
#############################


stacks, instructions = read_data('input.txt')

print(part_1(stacks, instructions))
print(part_2(stacks, instructions))
