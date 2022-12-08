from itertools import tee, islice


nwise_set = lambda iterbl, n: ((k, set(items)) 
                    for k, items in enumerate(zip(*[islice(itr, i, None) 
                            for i, itr in enumerate(tee(iterbl, n))])))


def find_start_marker(data, *, unique_num):
    for k, seq in nwise_set(data, unique_num):
        if len(seq) == unique_num:
            return k + unique_num


def part_1(data):
    return find_start_marker(data, unique_num=4)


def part_2(data):
    return find_start_marker(data, unique_num=14)


def read_data(filename):
    with open(filename) as f:
        data = f.read().strip()
    return data


data = read_data('input.txt')
print(part_1(data))
print(part_2(data))


####################
assert part_1('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 7
assert part_1('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
assert part_1('nppdvjthqldpwncqszvftbrmjlhg') == 6
assert part_1('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 10
assert part_1('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11

assert part_2('mjqjpqmgbljsphdztnvjfqwrcgsmlb') == 19
assert part_2('bvwbjplbgvbhsrlpgdmjqwftvncz') == 23
assert part_2('nppdvjthqldpwncqszvftbrmjlhg') == 23
assert part_2('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 29
assert part_2('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 26
