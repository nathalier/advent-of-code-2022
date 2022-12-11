import re
from operator import mul, pow
from copy import deepcopy
from heapq import nlargest
from math import lcm


def play(barrel, worry_divider, normalizer, rounds):
    for n in range(rounds):
        for monkey in barrel:
            throws = monkey.throw_to_monkeys(worry_divider, normalizer)
            for item, monk_num in throws:
                barrel[monk_num].add_item(item)
            monkey.throw_all_items()
    return mul(*nlargest(2, [monkey.thrown_num for monkey in barrel]))


def part_1(barrel, normalizer):
    return play(barrel, worry_divider=3, normalizer=normalizer, rounds=20)
    

def part_2(barrel, normalizer):
    return play(barrel, worry_divider=1, normalizer=normalizer, rounds=10000)


def read_data(filename):
    with open(filename) as f:
        barrel, dividers = [], []
        while line := f.readline():
            if line.strip().startswith('Monkey'):
                monkey_num = int(re.match('^.*(\d+)', line).groups()[0])
            elif line.strip().startswith('Starting items'):
                monkey_items = list(map( int, re.findall('(\d+)', line)))
            elif line.strip().startswith('Operation'):
                operation = re.match('^.*(\+|\*) (\d+|old)', line).groups()
                if operation[1] == 'old':
                    monkey_op = lambda x: pow(x, 2)
                else:
                    monkey_op = eval(f'lambda x: (x {operation[0]} {operation[1]})')
            elif line.strip().startswith('Test'):
                divider = int(re.match('^.*divisible by (\d+)', line).groups()[0])
                dividers.append(divider)
                true_line = f.readline().strip()
                true_res = int(re.match('^If true: throw to monkey (\d+)', true_line).groups()[0])
                false_line = f.readline().strip()
                false_res = int(re.match('^If false: throw to monkey (\d+)', false_line).groups()[0])
                throw_to = eval(f'lambda x: {true_res} if x % {divider} == 0 else {false_res}')
                barrel.append(Monkey(monkey_num, monkey_items, monkey_op, throw_to))
    return barrel, lcm(*dividers)


class Monkey:
    def __init__(self, monkey_num, items, operation, throw_to):
        self.num = monkey_num
        self.items = items
        self.operation = operation
        self.throw_to = throw_to
        self.thrown_num = 0

    def add_item(self, item):
        self.items.append(item)

    def throw_all_items(self):
        self.thrown_num += len(self.items)
        self.items = []        

    def throw_to_monkeys(self, worry_divider, normilizer):
        items = list(map(self.operation, self.items))
        worry_adjusted_items = list(map(lambda x: x // worry_divider % normilizer, items))
        throw_to_monkeys = list(map(self.throw_to, worry_adjusted_items))
        return list(zip(worry_adjusted_items, throw_to_monkeys))

    def __str__(self):
        return self.items


#############################
test_monkeys, normalizer = read_data('input_t.txt')

assert part_1(deepcopy(test_monkeys), normalizer) == 10605
assert part_2(deepcopy(test_monkeys), normalizer) == 2713310158
#############################

monkeys, normalizer = read_data('input.txt')

print(part_1(deepcopy(monkeys), normalizer))
print(part_2(deepcopy(monkeys), normalizer))
