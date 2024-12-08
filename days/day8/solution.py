import sys
from itertools import product
from pathlib import Path

type Point = tuple[int, int]


def part_1(raw_input: str) -> float:
    antenna_points_by_key, dim = parse_input(raw_input)
    return len(get_anti_nodes(antenna_points_by_key, dim, False))


def part_2(raw_input: str) -> float:
    antenna_points_by_key, dim = parse_input(raw_input)
    return len(get_anti_nodes(antenna_points_by_key, dim, True))


def parse_input(raw_input: str) -> tuple[dict[str, list[Point]], tuple[int, int]]:
    antenna_points_by_key = {}
    mx = raw_input.splitlines()
    n, m = len(mx), len(mx[0])
    for i, row in enumerate(mx):
        for j, char in enumerate(row):
            if char != ".":
                antenna_points_by_key[char] = antenna_points_by_key.get(char, []) + [
                    (i, j)
                ]
    return antenna_points_by_key, (n, m)


def get_anti_nodes(
    antenna_points_by_key: dict[str, list[Point]], dim: tuple[int, int], repeat: bool
):
    anti_nodes = []
    for key in antenna_points_by_key:
        antennas = antenna_points_by_key[key]
        [
            get_anti_nodes_for_points(x, y, dim, repeat, anti_nodes, set())
            for x, y in product(antennas, antennas)
            if x < y
        ]
    return set(anti_nodes)


def get_anti_nodes_for_points(
    p1: Point,
    p2: Point,
    dim: tuple[int, int],
    repeat: bool,
    anti_nodes: list[Point],
    visited: set[Point],
):
    (x1, y1), (x2, y2) = p1, p2
    c1, c2 = (2 * x1 - x2, 2 * y1 - y2), (2 * x2 - x1, 2 * y2 - y1)
    is_c1_valid = c1 not in visited and 0 <= c1[0] < dim[0] and 0 <= c1[1] < dim[1]
    is_c2_valid = c2 not in visited and 0 <= c2[0] < dim[0] and 0 <= c2[1] < dim[1]
    anti_nodes += ([c1] if is_c1_valid else []) + ([c2] if is_c2_valid else [])
    if repeat:
        anti_nodes += [p1, p2]
        visited.update([p1, p2])
        if is_c1_valid:
            get_anti_nodes_for_points(p1, c1, dim, True, anti_nodes, visited)
        if is_c2_valid:
            get_anti_nodes_for_points(p2, c2, dim, True, anti_nodes, visited)


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
