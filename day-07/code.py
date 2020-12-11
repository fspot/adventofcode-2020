import json
from pathlib import Path
from typing import List, Optional, Set

lines = Path('input.txt').read_text().splitlines(keepends=False)

mapping: dict = {}
all_available_colors: Set[str] = set()


def full_available_content(
    parent_color: str, current_content: Optional[Set[str]] = None
) -> List[str]:
    """Returns the list of colors which can be carried by a parent color (recursively)"""
    current_content = current_content or set()
    child_colors = list(mapping[parent_color].keys())
    for cc in child_colors:
        current_content.add(cc)
        full_available_content(cc, current_content)  # append recursively
    return list(current_content)


def who_contains(child_color: str) -> List[str]:
    res: List[str] = []
    for c in all_available_colors:
        if child_color in full_available_content(c):
            res.append(c)
    return res


def recursive_bag_count(bag_color: str) -> int:
    if bag_color not in mapping or mapping[bag_color] == {}:
        print('Return early for', bag_color)
        return 1
    children = mapping[bag_color]
    child_sum = 0
    for child_color, child_count in children.items():
        print(bag_color, 'contains', child_count, child_color, 'bags')
        child_sum += child_count * recursive_bag_count(child_color)
        print('Sum is now', child_sum)
    print('Returning', child_sum)
    return 1 + child_sum


for line in lines:
    line = line[:-1]
    color = ' '.join(line.split()[:2])
    if color in mapping:
        raise ValueError(f'{color} already in mapping')
    mapping[color] = {}
    all_available_colors.add(color)

    contains = line.split(' contain ')[1].split(', ')
    if len(contains) == 1 and contains[0].startswith('no other bags'):
        continue
    for contained in contains:
        nb = int(contained.split()[0])
        contained_color = ' '.join(contained.split()[1:3])
        mapping[color][contained_color] = nb
        all_available_colors.add(contained_color)

print(json.dumps(mapping, indent=2))
print(len(who_contains('shiny gold')))
print(recursive_bag_count('shiny gold') - 1)
