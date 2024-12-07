import copy
import sys
from pathlib import Path

type Position = tuple[int, int]
type Direction = tuple[int, int]


def part_1(raw_input: str) -> float:
    m, p = parse_input(raw_input)
    visited = set()
    patrol(m, p, visited)
    return len(visited)


def part_2(raw_input: str) -> float:
    m, sp = parse_input(raw_input)
    obstructions: list[Position] = []
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] != ".":
                continue
            new_m = place_obstruction(m, (i, j))
            if patrol(new_m, sp, set()):
                obstructions.append((i, j))
    return len(obstructions)


def parse_input(raw_input: str) -> tuple[list[list[str]], Position]:
    m = [list(line) for line in raw_input.splitlines()]
    for i, row in enumerate(m):
        for j, c in enumerate(row):
            if c == "^":
                return m, (i, j)


def is_in_map(p: Position, m: list[list[str]]):
    n, m = len(m), len(m[0])
    i, j = p[0], p[1]
    return 0 <= i < n and 0 <= j < m


def patrol(m: list[list[str]], start: Position, visited: set[Position]) -> bool:
    p, d, confs = tuple(start), (-1, 0), set()
    while is_in_map(p, m):
        if is_loop(confs, p, d):
            return True

        if m[p[0]][p[1]] != "#":
            confs.add((p, d))
            visited.add(p)
            p = tuple(a + b for a, b in zip(p, d))
        else:
            p = tuple(a - b for a, b in zip(p, d))
            d = (d[1], -d[0])
    return False


def is_loop(confs: set[tuple[Position, Direction]], p: Position, d: Direction):
    return (p, d) in confs


def place_obstruction(m: list[list[str]], p: Position):
    new_m = copy.deepcopy(m)
    new_m[p[0]][p[1]] = "#"
    return new_m


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
