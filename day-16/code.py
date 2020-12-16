from copy import deepcopy
from math import prod
from pathlib import Path
from typing import List, Tuple


class Rule:
    def __init__(self, line: str):
        self.name, line = line.split(':', 1)
        ranges = line.strip().split(' or ')
        rules = [[int(i) for i in r.split('-')] for r in ranges]
        self.rules: List[Tuple[int, int]] = rules  # type: ignore

    def validate(self, x: int) -> bool:
        for rule in self.rules:
            if rule[0] <= x <= rule[1]:
                return True
        return False


class Ticket:
    def __init__(self, line: str):
        self.values = [int(i) for i in line.split(',')]

    def get_invalid_values(self, rules: List[Rule]) -> List[int]:
        return [x for x in self.values if not any(r.validate(x) for r in rules)]


class Solution:
    def __init__(self, rules: List[Rule], tickets: List[Ticket]):
        field_names = [r.name for r in rules]
        self.rules_map = {r.name: r for r in rules}
        self.tickets = tickets
        self.possibilities: List[List[str]] = [deepcopy(field_names) for _ in field_names]
        self.indexes_still_unknown = list(range(len(field_names)))

    def get_possibilities(self, field_index: int) -> List[str]:
        return list(self.possibilities[field_index])

    def possibility_found(self, field_index: int, field_name: str):
        self.indexes_still_unknown.remove(field_index)
        # Remove this possibility for *other* indexes:
        for idx in list(self.indexes_still_unknown):
            if field_name in self.possibilities[idx]:
                self.remove_possibility(idx, field_name)

    def remove_possibility(self, field_index: int, field_name: str):
        possibilities_for_index = self.possibilities[field_index]
        possibilities_for_index.remove(field_name)

        if len(possibilities_for_index) == 1:
            # We found the name for this index!
            name = possibilities_for_index[0]
            self.possibility_found(field_index, name)

    def solve(self):
        for t in self.tickets:
            for idx in list(self.indexes_still_unknown):
                value = t.values[idx]
                for field_name in self.get_possibilities(idx):
                    rule = self.rules_map[field_name]
                    if not rule.validate(value):
                        self.remove_possibility(idx, field_name)

    def display(self):
        for i, field_names in enumerate(self.possibilities):
            print('Field num', i, 'can be any from:', field_names)

    def part2(self, ticket):
        departure_indexes = [
            i for i, poss in enumerate(self.possibilities) if poss[0].startswith('departure')
        ]
        return prod([ticket.values[idx] for idx in departure_indexes])


if __name__ == '__main__':
    lines = Path('input.txt').read_text().strip().split('\n\n')
    rules, my_ticket, other_tickets = lines
    rules = [Rule(line) for line in rules.splitlines(keepends=False)]
    other_tickets = [Ticket(line) for line in other_tickets.splitlines(keepends=False)[1:]]
    print('Part1:', sum([sum(t.get_invalid_values(rules)) for t in other_tickets]))

    # Part 2
    other_tickets = [t for t in other_tickets if not t.get_invalid_values(rules)]
    solution = Solution(rules, other_tickets)
    solution.solve()
    solution.display()
    print(solution.part2(Ticket(my_ticket.splitlines(keepends=False)[1])))
