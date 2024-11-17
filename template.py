import sys
from pathlib import Path


def part_1(raw_input: str) -> float:
    parse_input(raw_input)
    return 0


def part_2(raw_input: str) -> float:
    parse_input(raw_input)
    return 0


def parse_input(raw_input: str) -> list[str]:
    return raw_input.splitlines()


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1": print(part_1(current_input))
    case "2": print(part_2(current_input))
