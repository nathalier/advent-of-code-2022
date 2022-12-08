import re


def part_1(data):
    overlaped_num = 0
    for elves_task in data:
        matcher = re.match('^(\d*)-(\d*),(\d*)-(\d*)$', elves_task)
        start_1, end_1, start_2, end_2 = tuple(map(int, matcher.groups()))
        overlaped_num += fully_overlaped(start_1, end_1, start_2, end_2)
    return overlaped_num


def fully_overlaped(start_1, end_1, start_2, end_2):
    return start_1 <= start_2 <= end_1 and start_1 <= end_2 <= end_1 or\
           start_2 <= start_1 <= end_2 and start_2 <= end_1 <= end_2


def part_2(data):
    overlaped_num = 0
    for elves_task in data:
        matcher = re.match('^(\d*)-(\d*),(\d*)-(\d*)$', elves_task)
        start_1, end_1, start_2, end_2 = tuple(map(int, matcher.groups()))
        overlaped_num += overlaped(start_1, end_1, start_2, end_2)
    return overlaped_num


def overlaped(start_1, end_1, start_2, end_2):
    return start_1 <= start_2 <= end_1 or start_1 <= end_2 <= end_1 or\
           start_2 <= start_1 <= end_2 or start_2 <= end_1 <= end_2


def read_data(filename):
    with open(filename) as f:
        data = list(map(lambda x: x.strip(), f.readlines()))
    return data


#############################
test_data = read_data('input_t.txt')

assert part_1(test_data) == 2
assert part_2(test_data) == 4
#############################


data = read_data('input.txt')

print(part_1(data))
print(part_2(data))
