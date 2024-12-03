import re
import sys
from pathlib import Path


def part_1(raw_input: str) -> float:
    commands = parse_input(raw_input, False)
    return sum(list(map(multiply, commands)))


def part_2(raw_input: str) -> float:
    commands = parse_input(raw_input, True)
    filtered_commands = filter_disabled_commands(commands)
    return sum(list(map(multiply, filtered_commands)))


def parse_input(raw_input: str, allow_conditional_commands: bool) -> list[str]:
    if allow_conditional_commands:
        return re.findall(r"mul\(\d{1,3},\d{1,3}\)|don\'t\(\)|do\(\)", raw_input)
    else:
        return re.findall(r"mul\(\d{1,3},\d{1,3}\)", raw_input)


def multiply(command: str) -> int:
    sp1, sp2 = re.match(r"mul\((\d{1,3}),(\d{1,3})\)", command).groups()
    p1, p2 = int(sp1), int(sp2)
    return p1 * p2


def filter_disabled_commands(commands: list[str]) -> list[str]:
    filtered_commands = []
    is_enable = True
    for command in commands:
        if "don't" in command:
            is_enable = False
            continue

        if "do" in command:
            is_enable = True
            continue

        if "mul" in command and is_enable:
            filtered_commands.append(command)

    return filtered_commands


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
