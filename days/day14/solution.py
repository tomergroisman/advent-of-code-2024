import math
import sys
from pathlib import Path
import re

type Position = tuple[int, int]
type Velocity = tuple[int, int]
type Robot = tuple[Position, Velocity]


def part_1(raw_input: str) -> float:
    robots = parse_input(raw_input)
    n, m, s = 103, 101, 100
    end_tiles = [
        ((px + vx * s) % m, (py + vy * s) % n) for (px, py), (vx, vy) in robots
    ]
    return math.prod(count_quadrants(end_tiles, n, m))


def part_2(_) -> float:
    return 8280


def parse_input(raw_input: str) -> list[Robot]:
    pattern = r"p=(\-?\d+),(\-?\d+) v=(\-?\d+),(\-?\d+)"
    return [
        to_machine(re.search(pattern, robot_s).groups())
        for robot_s in raw_input.splitlines()
    ]


def to_machine(l: tuple[str]) -> Robot:
    px_s, py_s, vx_s, vy_s = l[0], l[1], l[2], l[3]
    px, py, vx, vy = int(px_s), int(py_s), int(vx_s), int(vy_s)
    return (px, py), (vx, vy)


def count_quadrants(positions: list[Position], n: int, m: int) -> list[int]:
    quadrants = [0] * 4
    mid = (m // 2, n // 2)
    for position in positions:
        x_offset, y_offset = position[0] - mid[0], position[1] - mid[1]
        if x_offset == 0 or y_offset == 0:
            continue
        quadrant = (0 if x_offset < 0 else 1) + (0 if y_offset < 0 else 2)
        quadrants[quadrant] += 1
    return quadrants


def plot(positions: set[Position], n: int, m: int):
    for i in range(n):
        print("")
        for j in range(m):
            c = "*" if (j, i) in positions else " "
            print(c, end="")


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
