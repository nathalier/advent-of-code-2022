from itertools import zip_longest, chain, repeat
from functools import total_ordering
from operator import mul
from timeit import timeit


def part_1(data):
    return sum([i + 1 for i, ordered in enumerate(pair[0] < pair[1] for pair in data) if ordered])


def part_2(data):
    items_of_interest = [Item([[2]]), Item([[6]])]

    sorted_sygnals = sorted(data + items_of_interest)
    return mul(*[sorted_sygnals.index(item) + 1 for item in items_of_interest])


def part_2_faster(data):
    res = 1
    items_of_interest = [Item([[2]]), Item([[6]])]
    extended_data = data + items_of_interest

    for item in items_of_interest:
        res *= (sum([1 for ordered in (pair[0] <= pair[1] for pair in zip(extended_data, repeat(item))) if ordered]))
    
    return res


@total_ordering
class Item:
    def __init__(self, value) -> None:
        self.value = value

    def __eq__(self, other) -> bool:
        return Item._compare_lists(self.value, other.value) == 0

    def __lt__(self, other) -> bool:
        return Item._compare_lists(self.value, other.value) == -1

    @staticmethod
    def _compare_lists(left, right):
        if not left and not right:
            return 0
        for l, r in zip_longest(left, right):
            if (res := Item._compare_one(l, r)) != 0:
                break
        return res

    @staticmethod
    def _compare_one(l_item, r_item):
        if None in [l_item, r_item]:
            return -1 if l_item is None else 1
        elif isinstance(l_item, int) and isinstance(r_item, int):
            return -1 if l_item < r_item else 0 if l_item == r_item else 1
        else:
            return Item._compare_lists(
                *list(map(lambda x: [x] if isinstance(x, int) else x, [l_item, r_item])))


def read_data(filename):
    with open(filename) as f:
        data = list(map(lambda x: tuple(map(lambda x: Item(eval(x)), x.split('\n'))), 
                        f.read().split('\n\n')))
    return data


#############################
test_data = read_data('input_t.txt')
flattened_test_data = list(chain(*test_data))

assert (res := part_1(test_data)) == 13, f'Actual: {res}'
assert (res := part_2(flattened_test_data)) == 140, f'Actual: {res}'
assert (res := part_2_faster(flattened_test_data)) == 140, f'Actual: {res}'
#############################


data = read_data('input.txt')
flattened_data = list(chain(*data))

print(part_1(data))
print(part_2(flattened_data))
print(part_2_faster(flattened_data))

print('part_2 v.1: ', timeit('part_2(flattened_data)', number=100, globals=globals()))
print('part_2 v.2 (faster): ', timeit('part_2_faster(flattened_data)', number=100, globals=globals()))

# part_2 v.1:           5.477586299995892
# part_2 v.2 (faster):  0.9202602000004845
