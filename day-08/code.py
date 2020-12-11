from copy import deepcopy
from pathlib import Path

NOP, ACC, JMP = 'nop', 'acc', 'jmp'


class InfiniteLoop(Exception):
    pass


class Computer:
    def __init__(self, lines):
        self.current_pos = 0
        self.position_history = []
        self.accumulator = 0
        self.memory = []
        for line in lines:
            op, value = line.split()
            assert op in (NOP, ACC, JMP)
            value = int(value)
            self.memory.append((op, value))

    def execute_nop(self, value):
        self.current_pos += 1

    def execute_acc(self, value):
        self.accumulator += value
        self.current_pos += 1

    def execute_jmp(self, value):
        self.current_pos += value

    def execute_one_operation(self):
        current_pos = self.current_pos
        memory_cell = self.memory[self.current_pos]
        op, value = memory_cell
        if op == NOP:
            self.execute_nop(value)
        elif op == ACC:
            self.execute_acc(value)
        elif op == JMP:
            self.execute_jmp(value)
        self.position_history.append(current_pos)

    def run(self):
        while True:
            if self.current_pos in self.position_history:
                raise InfiniteLoop()
            self.execute_one_operation()
            if self.current_pos == len(self.memory):
                print('Program terminates!')
                break


def try_program(lines):
    c = Computer(lines)
    try:
        c.run()
    except InfiniteLoop:
        return False
    print('Success:', c.accumulator)
    return True


def generate_variants(lines):
    for i in range(len(lines)):
        line = lines[i]
        if line.startswith('acc'):
            continue
        if line.startswith('nop'):
            modified_line = line.replace('nop', 'jmp')
        elif line.startswith('jmp'):
            modified_line = line.replace('jmp', 'nop')
        variant = deepcopy(lines)
        variant[i] = modified_line
        print('Yielding variant for line:', i)
        yield variant


lines = Path('input.txt').read_text().splitlines(keepends=False)
for variant in generate_variants(lines):
    if try_program(variant):
        print('Yass')
        break
