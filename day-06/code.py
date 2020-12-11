from collections import Counter
from pathlib import Path

groups = Path('input.txt').read_text().split('\n\n')

total = 0

for group in groups:
    group_answers = []
    users = group.splitlines(keepends=False)
    nb_users = len(users)
    for user in users:
        answers = list(user)
        group_answers += answers
    counter = Counter(group_answers)
    group_answers_count = sum([v == nb_users for v in counter.values()])
    total += group_answers_count

print(total)
