import re
from pathlib import Path
from typing import Dict, List, Union
from dataclasses import dataclass

WRITEVALUE_PATTERN = re.compile(r"mem\[(\d+)\] \= (\d+)")


def apply_mask(value: int, mask: str) -> int:
    mask_enforce_ones = int(mask.replace("X", "0"), 2)
    value |= mask_enforce_ones
    mask_enforce_zeros = int(mask.replace("X", "1"), 2)
    value &= mask_enforce_zeros
    return value


@dataclass
class SetMask:
    mask: str


@dataclass
class WriteValue:
    addr: int
    value: int


Command = Union[SetMask, WriteValue]


def parse_program(lines: List[str]) -> List[Command]:
    program: List[Command] = []
    for line in lines:
        if line.startswith("mask"):
            mask = line.split(" = ")[1]
            program.append(SetMask(mask=mask))
        elif match := WRITEVALUE_PATTERN.fullmatch(line):
            groups = match.groups()
            addr, value = int(groups[0]), int(groups[1])
            program.append(WriteValue(addr=addr, value=value))
        else:
            raise ValueError(line)
    return program


class Computer:
    def __init__(self, commands: List[str]):
        self.mask = "X" * 36
        self.program = parse_program(lines)
        self.memory: Dict[int, int] = {}

    def run_command(self, command: Command):
        if isinstance(command, SetMask):
            self.mask = command.mask
        elif isinstance(command, WriteValue):
            self.memory[command.addr] = apply_mask(command.value, self.mask)

    def run_full_program(self):
        for command in self.program:
            self.run_command(command)

    def get_sum_memory(self):
        return sum(self.memory.values())


if __name__ == "__main__":
    lines = Path("input.txt").read_text().splitlines(keepends=False)
    computer = Computer(lines)
    computer.run_full_program()
    print("Part1:", computer.get_sum_memory())
