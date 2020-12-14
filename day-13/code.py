import math
from functools import reduce
from operator import mul
from pathlib import Path
from typing import List, Tuple


Constraints = List[Tuple[int, int]]  # Tuple[offset, bus_id]


def next_available_depart(min_depart: int, bus_id: int) -> int:
    return math.ceil(min_depart / bus_id) * bus_id


def part1(lines):
    min_depart = int(lines[0])
    bus_ids = [int(i) for i in lines[1].split(",") if i != "x"]
    departs = {bus_id: next_available_depart(min_depart, bus_id) for bus_id in bus_ids}
    first_depart = sorted(departs.items(), key=lambda e: e[1])[0]
    bus_id = first_depart[0]
    wait_time = first_depart[1] - min_depart
    print("Res:", bus_id * wait_time)


def all_constraints_are_valid(constraints, t: int) -> bool:
    for i, bus_id in constraints:
        if (t + i) % bus_id != 0:
            return False
    return True


def solve2_attempt1(constraints):
    t = 0
    max_idx, max_bus_id = sorted(constraints, key=lambda e: e[1])[-1]
    print("Step:", max_bus_id)
    while True:
        try:
            if all_constraints_are_valid(constraints, t - max_idx):
                print("Res2:", t - max_idx)
                break
            t += max_bus_id
        except KeyboardInterrupt:
            print("Abort:", t)
            return


"""
# Attempt 2: using optlang (constraint solver) → slower than attempt 1
s = '7,13,x,x,59,x,31,19'

bus_ids = s.split(',')
constraints = []
for i, bus_id in enumerate(bus_ids):
    if bus_id == 'x':
        continue
    constraints.append((i, int(bus_id)))

t = Variable('t', lb=0, type='integer')
variables = [t]
optlang_constraints = []
for i, c in enumerate(constraints):
    v = Variable(f'x{i}', lb=0, type='integer')
    variables.append(v)
    c = Constraint(c[1] * v - t, lb=c[0], ub=c[0])
    optlang_constraints.append(c)

obj = Objective(t, direction='min')

model = Model(name='Simple model')
model.objective = obj
model.add(optlang_constraints)

status = model.optimize()

print("status:", model.status)
print("objective value:", model.objective.value)
print("----------")
for var_name, var in model.variables.iteritems():
    print(var_name, "=", var.primal)
"""

# Attempt 3


def get_step(constraints_ok: Constraints):
    return reduce(mul, [e[1] for e in constraints_ok], 1)


def get_valid_constraints(constraints: Constraints, t: int) -> Constraints:
    valid_constraints = []
    for constraint in constraints:
        i, bus_id = constraint
        if (t + i) % bus_id == 0:
            valid_constraints.append(constraint)
    return valid_constraints


def solve2(constraints: Constraints):
    t = 0
    while True:
        valid_constraints = get_valid_constraints(constraints, t)
        if len(valid_constraints) == len(constraints):
            return t
        step = get_step(valid_constraints)
        t += step


def part2(lines):
    bus_ids = lines[1].split(",")
    constraints = []
    for i, bus_id in enumerate(bus_ids):
        if bus_id == "x":
            continue
        constraints.append((i, int(bus_id)))
    t = solve2(constraints)
    print("All constraints are valid at t =", t)


if __name__ == "__main__":
    lines = Path("input.txt").read_text().splitlines(keepends=False)
    part1(lines)
    part2(lines)
