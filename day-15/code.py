from collections import defaultdict, deque
from pathlib import Path
from typing import Deque, Dict, List


class Game:
    def __init__(self, starting_numbers: List[int], nb_turns: int):
        self.starting_numbers = starting_numbers
        self.nb_turns = nb_turns
        self.current_turn = 0
        self.last_number = 0
        self.last_positions: Dict[int, Deque[int]] = defaultdict(
            lambda: deque([], maxlen=2)
        )

    def play_1_turn(self) -> int:
        if self.current_turn < len(self.starting_numbers):
            return self.starting_numbers[self.current_turn]

        last_positions = self.last_positions[self.last_number]
        if len(last_positions) < 2:
            return 0

        return last_positions[-1] - last_positions[0]

    def play(self) -> int:
        for turn in range(self.nb_turns):
            if turn % 100_000 == 0:
                print("Current turn:", turn)

            self.current_turn = turn
            value = self.play_1_turn()
            self.last_positions[value].append(turn)
            self.last_number = value

        return self.last_number


if __name__ == "__main__":
    starting_numbers = [
        int(i) for i in Path("input.txt").read_text().strip().split(",")
    ]
    print("Part1:", Game(starting_numbers, 2020).play())
    print("Part2:", Game(starting_numbers, 30_000_000).play())
