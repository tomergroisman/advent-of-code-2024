import sys
import re
from pathlib import Path
import sympy
from sympy.abc import x, y

type Point = tuple[int, int]
type Button = tuple[int, int]
type Machine = tuple[Button, Button, Point]


def part_1(raw_input: str) -> float:
    machines, total_cost = parse_input(raw_input), 0
    for m in machines:
        a, b, r = m[0], m[1], m[2]
        total_cost += calc_min_cost(a, b, r, 0)
    return total_cost


def part_2(raw_input: str) -> float:
    offset = 10000000000000
    machines, total_cost = parse_input(raw_input), 0
    for m in machines:
        a, b, r = m[0], m[1], m[2]
        total_cost += calc_min_cost(a, b, r, offset)
    return total_cost


def parse_input(raw_input: str) -> list[Machine]:
    machine_pattern = r"Button A: X\+(\d+), Y\+(\d+)\|Button B: X\+(\d+), Y\+(\d+)\|Prize: X=(\d+), Y=(\d+)"
    return [
        to_tuples_of_2(
            list(
                map(
                    int,
                    re.search(machine_pattern, machine_s.replace("\n", "|")).groups(),
                )
            )
        )
        for machine_s in raw_input.split("\n\n")
    ]


def to_tuples_of_2(l: list[int]):
    return tuple([(l[i], l[i + 1]) for i in range(0, len(l) - 1, 2)])


def calc_min_cost(
    a: tuple[int, int],
    b: tuple[int, int],
    r: tuple[int, int],
    offset: int,
):
    solution = sympy.solve(
        [a[0] * x + b[0] * y - r[0] - offset, a[1] * x + b[1] * y - r[1] - offset],
        [x, y],
    )
    if int(solution[x]) == solution[x] and int(solution[y]) == solution[y]:
        return solution[x] * 3 + solution[y]
    return 0


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
