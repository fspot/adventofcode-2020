from itertools import combinations

numbers = [int(i) for i in open('input.txt').readlines()]

for (x, y, z) in combinations(numbers, 3):
    if x + y + z == 2020:
        print(x * y * z)
