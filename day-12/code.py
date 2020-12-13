import math
from pathlib import Path
from typing import List, Tuple


def rotate(point: Tuple[float, float], degrees: float) -> Tuple[float, float]:
    x, y = point
    radian = degrees * math.pi / 180
    current_norm = math.sqrt(x ** 2 + y ** 2)
    current_angle = math.atan2(y, x)
    new_angle = current_angle + radian
    new_x = current_norm * math.cos(new_angle)
    new_y = current_norm * math.sin(new_angle)
    return (new_x, new_y)


class Ship:
    def __init__(self, route: List[str]):
        self.route = route
        self.x = 0
        self.y = 0
        self.waypoint_x = 10
        self.waypoint_y = 1

    def run_step_north(self, value: int):
        self.waypoint_y += value

    def run_step_south(self, value: int):
        self.waypoint_y -= value

    def run_step_east(self, value: int):
        self.waypoint_x += value

    def run_step_west(self, value: int):
        self.waypoint_x -= value

    def run_step_left(self, value: int):
        self.waypoint_x, self.waypoint_y = rotate((self.waypoint_x, self.waypoint_y), value)

    def run_step_right(self, value: int):
        self.waypoint_x, self.waypoint_y = rotate((self.waypoint_x, self.waypoint_y), -value)

    def run_step_forward(self, value: int):
        self.x += value * self.waypoint_x
        self.y += value * self.waypoint_y

    def run_1_step(self, step: str):
        step_func = {
            'R': self.run_step_right,
            'L': self.run_step_left,
            'F': self.run_step_forward,
            'E': self.run_step_east,
            'W': self.run_step_west,
            'S': self.run_step_south,
            'N': self.run_step_north,
        }[step[0]]
        value = int(step[1:])
        step_func(value)
        print(step)
        print(self.x, self.y)

    def run_until_complete(self):
        for step in self.route:
            self.run_1_step(step)

    def manhatan_distance(self):
        return abs(self.x) + abs(self.y)


if __name__ == '__main__':
    lines = Path('input.txt').read_text().splitlines(keepends=False)
    ship = Ship(lines)
    ship.run_until_complete()
    print('Manhatan distance:', ship.manhatan_distance())
