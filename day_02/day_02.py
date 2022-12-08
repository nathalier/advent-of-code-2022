def part_1(data):
    game_tr_table = dict(tr_table, **{'X': 'R', 'Y': 'P', 'Z': 'S'})

    outcome = 0
    for line in data:
        game = tuple(map(lambda choice: game_tr_table[choice], line.split()))
        outcome += outcomes[game] + choice_points[game[1]]

    return outcome


def part_2(data):
    outcome_codes = {'X': 0, 'Y': 3, 'Z': 6} 
    outcome = 0
    for line in data:
        game = line.split()
        game[0] = tr_table[game[0]]
        game[1] = define_choice(game, outcome_codes)
        outcome += outcomes[tuple(game)] + choice_points[game[1]]
    return outcome


def define_choice(code, outcome_codes):
    x = list(filter(
        lambda item: item[0][0] == code[0] and item[1] == outcome_codes[code[1]], 
        outcomes.items()))
    return x[0][0][1]


def read_data(filename):
    with open(filename) as f:
        data = list(map(lambda x: x.strip(), f.readlines()))
    return data


outcomes = {
    ('R', 'R'): 3,
    ('R', 'P'): 6,
    ('R', 'S'): 0,
    ('P', 'R'): 0,
    ('P', 'P'): 3,
    ('P', 'S'): 6,
    ('S', 'R'): 6,
    ('S', 'P'): 0,
    ('S', 'S'): 3,
}

choice_points = {
    'R': 1,
    'P': 2,
    'S': 3,
}

tr_table = {
    'A': 'R',
    'B': 'P',
    'C': 'S',
}

#############################
test_data = read_data('input_t.txt')

assert part_1(test_data) == 15
assert part_2(test_data) == 12
#############################


data = read_data('input.txt')

print(part_1(data))
print(part_2(data))
