import sys
from pathlib import Path
from itertools import product

type Equation = tuple[list[int], int]


def part_1(raw_input: str) -> float:
    equations = parse_input(raw_input)
    return sum(
        [get_equation_calibration_value(equation, False) for equation in equations]
    )


def part_2(raw_input: str) -> float:
    equations = parse_input(raw_input)
    return sum(
        [get_equation_calibration_value(equation, True) for equation in equations]
    )


def parse_input(raw_input: str) -> list[Equation]:
    return [
        (list(map(int, nums.split(" "))), int(test_v))
        for test_v, nums in [row.split(": ") for row in raw_input.splitlines()]
    ]


def get_equation_calibration_value(equation: Equation, extended_ops: bool):
    nums, test_v = equation
    length = len(nums) - 1
    options = product(["+", "*"] + (["|"] if extended_ops else []), repeat=length)
    for option in options:
        if is_equation_valid(equation, option):
            return test_v
    return 0


def is_equation_valid(equation: Equation, ops: tuple[str, ...]):
    nums, test_v = equation
    s = nums[0]
    for i, op in enumerate(ops):
        if s > test_v:
            return False
        if op == "+":
            s += nums[i + 1]
        if op == "*":
            s *= nums[i + 1]
        if op == "|":
            s = int(str(s) + str(nums[i + 1]))
    return s == test_v


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
