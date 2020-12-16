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


if __name__ == '__main__':
    lines = Path('input.txt').read_text().strip().split('\n\n')
    rules, my_ticket, other_tickets = lines
    rules = [Rule(line) for line in rules.splitlines(keepends=False)]
    other_tickets = [Ticket(line) for line in other_tickets.splitlines(keepends=False)[1:]]
    print('Part1:', sum([sum(t.get_invalid_values(rules)) for t in other_tickets]))
