import sys
from pathlib import Path
import numpy as np

type Key = tuple[str]
type Lock = tuple[str]


def part_1(raw_input: str) -> float:
    locks, keys = parse_input(raw_input)
    s = 0
    for lock in locks:
        for key in keys:
            if all([a >= b for a, b in zip(lock, key)]):
                s += 1
    return s


def parse_input(raw_input: str) -> tuple[list[Lock], list[Key]]:
    schemas_str = raw_input.split("\n\n")
    locks, keys = [], []
    for schema_str in schemas_str:
        is_lock = schema_str[0][0] == "#"
        schema = np.rot90(np.array([list(s) for s in schema_str.splitlines()]), 1)[
            ::-1
        ].tolist()

        char = "." if is_lock else "#"
        pins = tuple([l.count(char) for l in schema if l])
        if is_lock:
            locks.append(pins)
        else:
            keys.append(pins)
    return locks, keys


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
