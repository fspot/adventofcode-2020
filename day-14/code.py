import re
from itertools import product
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


def apply_mask_v2(addr: int, mask: str) -> List[int]:
    # First, force the 1s on the address:
    mask_enforce_ones = int(mask.replace("X", "0"), 2)
    addr |= mask_enforce_ones
    # Then, apply floating bits:
    addresses = []
    combinations = product([0, 1], repeat=mask.count('X'))
    mask = mask.replace('0', '.').replace('1', '.').replace('X', '%d').replace('.', 'X')
    for comb in combinations:
        mask_for_comb = mask % comb
        addresses.append(apply_mask(addr, mask_for_comb))
    return addresses


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
    def __init__(self, commands: List[str], version: int = 1):
        self.mask = "X" * 36
        self.program = parse_program(lines)
        self.memory: Dict[int, int] = {}
        self.version = version

    def run_command_writevalue_v2(self, addr: int, value: int, mask: str):
        all_addresses = apply_mask_v2(addr, mask)
        for addr in all_addresses:
            self.memory[addr] = value

    def run_command(self, command: Command):
        if isinstance(command, SetMask):
            self.mask = command.mask
        elif isinstance(command, WriteValue):
            if self.version == 2:
                self.run_command_writevalue_v2(command.addr, command.value, self.mask)
            else:
                self.memory[command.addr] = apply_mask(command.value, self.mask)

    def run_full_program(self):
        for command in self.program:
            self.run_command(command)

    def get_sum_memory(self):
        return sum(self.memory.values())


if __name__ == "__main__":
    lines = Path("input.txt").read_text().splitlines(keepends=False)

    c1 = Computer(lines, version=1)
    c1.run_full_program()
    print("Part1:", c1.get_sum_memory())

    c2 = Computer(lines, version=2)
    c2.run_full_program()
    print("Part2:", c2.get_sum_memory())
