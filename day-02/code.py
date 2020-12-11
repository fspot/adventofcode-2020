from pathlib import Path

lines = Path('input.txt').read_text().splitlines(keepends=False)

total_right = 0

for line in lines:
    counts, char, password = line.split()
    posa, posb = [int(i) for i in counts.split('-')]
    char = char[0]
    founda, foundb = password[posa - 1] == char, password[posb - 1] == char
    if founda ^ foundb:
        print('Good line:', line)
        total_right += 1

print('Total right:', total_right)
