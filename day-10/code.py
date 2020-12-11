from collections import Counter
from operator import mul
from functools import reduce
from pathlib import Path

lines = Path('input.txt').read_text().splitlines(keepends=False)
ratings = [int(i) for i in lines]
laptop_rating = max(ratings) + 3
sorted_ratings = [0] + sorted(ratings) + [laptop_rating]


# Part A:

steps = []
for a, b in zip(sorted_ratings[:-1], sorted_ratings[1:]):
    difference = b - a
    steps.append(difference)
c = Counter(steps)
print(c)
print(f'{c[1]} * {c[3]} = {c[1] * c[3]}')


# Part B:

# We only have steps of 1s and 3s.
# After some trials, I sawed that the number of eligible
# paths in a chain of values of length N, all separated by 1-steps,
# is tribonacci(N).


def tribonacci(n: int) -> int:
    if n <= 2:
        return 1
    elif n == 3:
        return 2
    return tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n - 3)


steps_as_string = ''.join(str(i) for i in steps)  # '131113113133'
splitted = steps_as_string.split('3')  # ['1', '111', '11', '1', '', '']
chains_lengths = [len(chain) + 1 for chain in splitted]  # +1 for the first elem of the chain
possibilities = [tribonacci(n) for n in chains_lengths]
total_possibilities = reduce(mul, possibilities, 1)
print(total_possibilities)

"""
def get_steps(path: List[int]) -> List[int]:
    steps = []
    for a, b in zip(path[:-1], path[1:]):
        difference = b - a
        steps.append(difference)
    return steps


def contains_only_small_steps(path: List[int], maxstep=3) -> bool:
    steps = get_steps(path)
    return all(e <= maxstep for e in steps)


def get_all_eligible_paths(path: List[int]):
    result = []
    assert contains_only_small_steps(path, maxstep=1) is True
    for i in range(len(path)):
        subcombs = list(combinations(path, i + 1))
        for comb in subcombs:
            if comb[0] == path[0] and comb[-1] == path[-1] and contains_only_small_steps(comb):
                result.append(comb)
    return result
"""
