from heapq import nlargest


def part_1(data):
    return max(map(sum, data))


def part_2(data):
    return sum(nlargest(3, list(map(sum, data))))


def read_data(filename):
    with open(filename) as f:
        data = f.read().split('\n\n')
        elves_food = list(map(lambda x: list(map(int, x.strip().split('\n'))), data))
    return elves_food


#############################
test_data = read_data('input_t.txt')

assert part_1(test_data) == 24_000
assert part_2(test_data) == 45_000
#############################


data = read_data('input.txt')

print(part_1(data))
print(part_2(data))
