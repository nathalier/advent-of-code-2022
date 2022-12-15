import re
from operator import attrgetter
from copy import deepcopy
from collections import deque


class Interval:
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

    def __str__(self):
        return f'[{self.start}, {self.end}]'


class IntervalSet:
    def __init__(self, intervals=None) -> None:
        self.intervals = [] if intervals is None else list(intervals)
        self.normalize()

    def normalize(self):
        if len(self.intervals) < 2:
            return
        sorted_ivs = sorted(self.intervals, key=attrgetter('start'))
        simplified = [sorted_ivs[0]]
        for iv in sorted_ivs[1:]:
            if iv.start - simplified[-1].end <= 1:
                simplified[-1].end = max(simplified[-1].end, iv.end)
            else:
                simplified.append(iv)
        self.intervals = deque(simplified)

    def insert(self, other:Interval | list):
        if isinstance(other, list) and len(other) == 0:
            return
        self.intervals.append(other)
        self.normalize()

    def extend(self, other:'IntervalSet'):
        self.intervals.extend(other)
        self.normalize()

    def subtract(self, other:'IntervalSet'):
        for iv in other.intervals:
            self.extract(iv)

    def extract(self, other:Interval):
        idx = 0
        while idx < len(self.intervals) and self.intervals[idx].start <= other.end:
            if other.start > self.intervals[idx].end:
                continue
            if other.start <= self.intervals[idx].start and other.end >= self.intervals[idx].end:
                self.intervals.pop(idx)
                continue
            elif other.start <= self.intervals[idx].start and other.end < self.intervals[idx].end:
                self.intervals[idx] = Interval(other.end + 1, self.intervals[idx].end)
            else: # other.start > self.start
                old_interval = deepcopy(self.intervals[idx])
                self.intervals[idx] = Interval(self.intervals[idx].start, other.start-1)
                if other.end < old_interval.end:
                    idx += 1
                    self.intervals.insert(idx, Interval(other.end+1, old_interval.end))
            idx += 1

    def __len__(self):
        return sum(map(lambda iv: iv.end - iv.start + 1, self.intervals))

    def __str__(self):
        return str(self.intervals)


def covered_in_row(covered_dist, row):
    sensors_covering_row = {s: d for s, d in covered_dist.items() if abs(row - s[1]) <= covered_dist[s]}
    covered_in_row = IntervalSet()
    for sensor in sensors_covering_row:
        covered_in_row.insert(covered_intervals(sensor, covered_dist[sensor], row))
    return covered_in_row


def covered_intervals(sensor, dist, row):
        if abs(sensor[1] - row) <= dist:
            width = 1 + (dist - abs(sensor[1] - row)) * 2
            start = sensor[0] - width // 2
            return Interval(start, start + width - 1)
        else:
            return []


def manhattan_dist(a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])


def part_1(mapa, y):
    covered_dist = {sensor: manhattan_dist(sensor, mapa[sensor]) for sensor in mapa.keys()}
    covered_row = covered_in_row(covered_dist, y)

    beacons = set(mapa.values())
    beacons_intervals = IntervalSet(list(map(lambda b: Interval(b[0], b[0]), 
                                      filter(lambda b: b[1] == y, beacons))))
    covered_row.subtract(beacons_intervals)

    return len(covered_row)


def part_2(mapa, board_size):
    covered_dist = {sensor: manhattan_dist(sensor, mapa[sensor]) for sensor in mapa.keys()}

    result = []
    for y in range(board_size[0], board_size[1] + 1):
        covered_row = covered_in_row(covered_dist, y)
        uncovered = IntervalSet([Interval(*board_size)])
        uncovered.subtract(covered_row)

        for iv in uncovered.intervals:
            result.extend([(x, y) for x in range(iv.start, iv.end + 1)])
    print(result)
    return result[0][0] * 4000000 + result[0][1]


def read_data(filename):
    mapa = {}
    with open(filename) as f:
        while line := f.readline().strip():
            positions = re.match('^.*x=(-?\d+).*y=(-?\d+).*x=(-?\d+).*y=(-?\d+)', line).groups()
            positions = list(map(int, positions))
            mapa[(positions[0], positions[1])] = (positions[2], positions[3])
    return mapa


#############################
test_data = read_data('input_t.txt')
test_board_size = [0, 20]

assert (res := part_1(test_data, y=10)) == 26, f'Actual: {res}'
assert (res := part_2(test_data, test_board_size)) == 56000011, f'Actual: {res}'
#############################


data = read_data('input.txt')
board_size = [0, 4_000_000]

print(part_1(data, y=2_000_000))
print(part_2(data, board_size))
