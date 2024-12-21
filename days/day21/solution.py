import itertools
import sys
from functools import cache
from math import inf
from pathlib import Path

type Position = tuple[int, int]


def part_1(raw_input: str) -> float:
    codes = parse_input(raw_input)
    return sum(int(code[:-1]) * get_shortest_sequence_length(code, 2) for code in codes)


def part_2(raw_input: str) -> float:
    codes = parse_input(raw_input)
    return sum(
        int(code[:-1]) * get_shortest_sequence_length(code, 25) for code in codes
    )


def parse_input(raw_input: str) -> list[str]:
    return raw_input.splitlines()


def get_shortest_sequence_length(code: str, depth: int):
    paths = get_keypad_paths(NUMERIC_A_POSITION, code, True)

    for i in range(depth):
        all_d_paths = []
        for n_path in paths:
            all_d_paths.extend(get_keypad_paths(DIRECTIONAL_A_POSITION, n_path, False))
        min_d_path_len = min([len(path) for path in all_d_paths])
        paths = [path for path in all_d_paths if len(path) == min_d_path_len]

    return len(paths[0])


def get_keypad_paths(start: Position, code: str, is_numeric: bool):
    prev, parts = start, []
    keymap = NUMERIC_POSITION_BY_KEY if is_numeric else DIRECTIONAL_POSITION_BY_KEY
    for key in code:
        parts.append(get_keypad_paths_to_key(prev, key, is_numeric))
        prev = keymap[key]
    return combine_shortest_parts(parts)


@cache
def get_keypad_paths_to_key(s: Position, key: str, is_numeric: bool):
    q, v = [(s, (0, 0), "")], set()
    keypad = NUMERIC_KEYPAD if is_numeric else DIRECTIONAL_KEYPAD
    n, m = len(keypad), len(keypad[0])
    paths, size = [], inf

    while q:
        c_p, c_d, path = q.pop(0)

        if len(path) > size:
            break

        c_key = keypad[c_p[0]][c_p[1]]
        if c_key == key:
            size = len(path)
            paths.append(path)

        for d in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            n_p = c_p[0] + d[0], c_p[1] + d[1]
            if 0 <= n_p[0] < n and 0 <= n_p[1] < m:
                n_key = keypad[n_p[0]][n_p[1]]
                if n_key != "#":
                    q.append((n_p, d, path + KEY_DIR_BY_DIR[d]))
    return paths


def combine_shortest_parts(parts: list[list[str]]):
    return list(
        "A".join(combination) + "A" for combination in itertools.product(*parts)
    )


NUMERIC_KEYPAD = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["#", "0", "A"],
]
NUMERIC_POSITION_BY_KEY = {
    "A": (3, 2),
    "0": (3, 1),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
}
DIRECTIONAL_KEYPAD = [
    ["#", "^", "A"],
    ["<", "v", ">"],
]
DIRECTIONAL_POSITION_BY_KEY = {
    "A": (0, 2),
    "^": (0, 1),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}
KEY_DIR_BY_DIR = {(-1, 0): "^", (0, 1): ">", (1, 0): "v", (0, -1): "<"}
NUMERIC_A_POSITION = NUMERIC_POSITION_BY_KEY["A"]
DIRECTIONAL_A_POSITION = DIRECTIONAL_POSITION_BY_KEY["A"]

input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
