from collections import deque
from itertools import combinations
from pathlib import Path

PREAMBLE_SIZE = 25

lines = Path('input.txt').read_text().splitlines(keepends=False)

# Part A

numbers = [int(i) for i in lines]
preamble = deque(numbers[:PREAMBLE_SIZE], PREAMBLE_SIZE)
numbers = numbers[PREAMBLE_SIZE:]


def check_respect_rule(number: int, preamble: deque) -> bool:
    for a, b in combinations(preamble, 2):
        if a + b == number:
            return True
    return False


for n in numbers:
    ok = check_respect_rule(n, preamble)
    if not ok:
        print(n, 'does not respect rule:', preamble)
        nok = n
    preamble.append(n)


# Part B

numbers = [int(i) for i in lines]

for i in range(len(numbers)):
    subset = numbers[i:]
    total = 0
    tryrange: deque = deque()
    for n in subset:
        total += n
        tryrange.append(n)
        if total > nok:
            continue  # the range does not start at index i
        elif total == nok and len(tryrange) != 1:
            print('Good range:', tryrange)
            print('Answer:', max(tryrange) + min(tryrange))
            break
