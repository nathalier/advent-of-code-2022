from string import ascii_letters


def part_1(data):
    total = 0
    for word in data:
        total += calculate_priority_1(word)
    return total


def calculate_priority_1(word):
    compartment_1 = word[: len(word) // 2]
    compartment_2 = word[len(word) // 2 :]
    common_item = set(compartment_1).intersection(set(compartment_2)).pop()
    return priorities[common_item]


def part_2(data):
    total, i = 0, 0
    for i in range(len(data) // 3):
        total += calculate_priority_2(data[3 * i: 3 * i + 3])
    return total


def calculate_priority_2(words):
    assert len(words) == 3
    common_item = set(words[0]).intersection(set(words[1])).intersection(set(words[2])).pop()
    return priorities[common_item]


def read_data(filename):
    with open(filename) as f:
        data = list(map(lambda x: x.strip(), f.readlines()))
    return data


priorities = {letter:val for letter, val in zip(ascii_letters, range(1, 53))}


#############################
test_data = read_data('input_t.txt')

assert part_1(test_data) == 157
assert part_2(test_data) == 70
#############################


data = read_data('input.txt')

print(part_1(data))
print(part_2(data))
