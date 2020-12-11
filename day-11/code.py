from copy import deepcopy
from pathlib import Path
from typing import List, Literal, Optional, Tuple

EMPTY_SPACE = "."
FREE_SEAT = "L"
OCCUPIED_SEAT = "#"
ALL_DIRECTIONS = [(-1, 0), (-1, -1), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
TOO_MUCH = 5  # was 4 in part 1

SeatOptions = Literal[FREE_SEAT, OCCUPIED_SEAT]
CellOptions = Literal[EMPTY_SPACE, FREE_SEAT, OCCUPIED_SEAT]
Matrix = List[List[Literal[EMPTY_SPACE, FREE_SEAT, OCCUPIED_SEAT]]]


class InfiniteLoop(Exception):
    pass


class World:
    def __init__(self, matrix: Matrix):
        self.matrix = deepcopy(matrix)
        self.previous_states: List[str] = []

    def get_value(self, x: int, y: int) -> Optional[CellOptions]:
        if y < 0 or x < 0 or y >= len(self.matrix) or x >= len(self.matrix[y]):
            return None  # out of bounds
        return self.matrix[y][x]

    def set_value(self, x: int, y: int, value: SeatOptions):
        self.matrix[y][x] = value

    def __str__(self) -> str:
        return "\n".join(["".join(line) for line in world.matrix])

    def display(self):
        print(str(self))
        print()

    def get_seeable_seat_values_from(self, x: int, y: int) -> List[Optional[CellOptions]]:
        def get_seeable_seat_in_direction(direction: Tuple[int, int]) -> Optional[CellOptions]:
            pos = (x, y)
            seeable = EMPTY_SPACE
            while seeable == EMPTY_SPACE:
                pos = (pos[0] + direction[0], pos[1] + direction[1])
                seeable = self.get_value(*pos)
            return seeable

        return [
            get_seeable_seat_in_direction(direction) for direction in ALL_DIRECTIONS
        ]

    def get_adjacent_seats(self, x: int, y: int) -> List[CellOptions]:
        # Part 1:
        # adjacent_values = [
        #     self.get_value(x - 1, y - 1),
        #     self.get_value(x - 1, y),
        #     self.get_value(x - 1, y + 1),
        #     self.get_value(x, y - 1),
        #     self.get_value(x, y + 1),
        #     self.get_value(x + 1, y - 1),
        #     self.get_value(x + 1, y),
        #     self.get_value(x + 1, y + 1),
        # ]
        # Part 2:
        adjacent_values = self.get_seeable_seat_values_from(x, y)
        return [value for value in adjacent_values if value is not None]

    def get_nb_adjacent_occupied_seats(self, x: int, y: int) -> int:
        return self.get_adjacent_seats(x, y).count(OCCUPIED_SEAT)

    def run_1_turn(self):
        current_world = World(self.matrix)  # clone the current state
        for y, line in enumerate(current_world.matrix):
            for x, _ in enumerate(line):
                if (
                    current_world.get_value(x, y) == FREE_SEAT
                    and current_world.get_nb_adjacent_occupied_seats(x, y) == 0
                ):
                    self.set_value(x, y, OCCUPIED_SEAT)
                elif (
                    current_world.get_value(x, y) == OCCUPIED_SEAT
                    and current_world.get_nb_adjacent_occupied_seats(x, y) >= TOO_MUCH
                ):
                    self.set_value(x, y, FREE_SEAT)

        if str(self) in self.previous_states:
            raise InfiniteLoop()

        # add the previous world to history:
        self.previous_states.append(str(current_world))

    def run_until_stable(self):
        while True:
            try:
                # self.display()
                self.run_1_turn()
            except InfiniteLoop:
                print("End.")
                break

    def get_nb_seats_occupied(self) -> int:
        return str(self).count(OCCUPIED_SEAT)


if __name__ == "__main__":
    lines = Path("input.txt").read_text().splitlines(keepends=False)
    matrix: Matrix = [list(line) for line in lines]
    world = World(matrix)
    world.run_until_stable()
    print(world.get_nb_seats_occupied())
