from pathlib import Path


class Map:
    def __init__(self, lines):
        self.lines = lines
        self.ymax = len(lines)
        self.x = 0
        self.y = 0
        self.total_trees = 0

    def __getitem__(self, key):
        x, y = key
        return self.lines[y][x]

    def __setitem__(self, key, value):
        x, y = key
        self.lines[y][x] = value

    def move(self, x, y):
        if self.y + y >= self.ymax:
            raise ValueError

        self.x += x
        self.y += y

        if self[self.x, self.y] == '#':
            self[self.x, self.y] = 'X'
            self.total_trees += 1
        else:
            self[self.x, self.y] = 'O'

    def display(self):
        for line in self.lines:
            print(''.join(line[:100]))  # maxsize of terminal


def try_slope(slope_x: int, slope_y: int) -> int:
    lines = Path('input.txt').read_text().splitlines(keepends=False)
    lines = [list(line * 1000) for line in lines]  # just repeat the pattern 1k times
    world = Map(lines)
    while True:
        try:
            world.move(slope_x, slope_y)
        except ValueError:
            break
    return world.total_trees


SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

res = 1

for (slope_x, slope_y) in SLOPES:
    nbtrees = try_slope(slope_x, slope_y)
    print(slope_x, slope_y, ' - Total trees:', nbtrees)
    res *= nbtrees

print('Result:', res)
