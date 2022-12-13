import numpy as np


def part_1(data):
    return ...


def part_2(data):
    return ...


def read_data(filename):
    with open(filename) as f:
        data = list(map(lambda x: x.strip(), f.readlines()))
    return data


#############################
test_data = read_data('input_t.txt')

assert (res := part_1(test_data)) == ..., f'Actual: {res}'
assert (res := part_2(test_data)) == ..., f'Actual: {res}'
#############################


data = read_data('input.txt')

print(part_1(data))
print(part_2(data))
