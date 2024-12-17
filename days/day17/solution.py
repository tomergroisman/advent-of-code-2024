import sys
from operator import xor
from pathlib import Path
import re

type Program = tuple[int, int, int, list[int]]
type MemoKey = tuple[int, int, int, int]


def part_1(raw_input: str) -> str:
    program, output = parse_input(raw_input), []
    run_program(program, output)
    return ",".join(str(n) for n in output)


def part_2(raw_input: str) -> float:
    (ra, rb, rc, instructions) = parse_input(raw_input)
    n = len(instructions) - 1
    res = 0

    for i in range(n, -1, -1):
        for j in range(8):
            if i == n and j == 0:
                continue

            output = []
            candidate = res + j * 8**i
            run_program((candidate, rb, rc, instructions), output)
            if output[i] == instructions[i]:
                res = candidate
                break

    while True:
        output = []
        run_program((res, rb, rc, instructions), output)
        if output == instructions:
            return res
        res += 1


def parse_input(raw_input: str) -> Program:
    program_s = raw_input.splitlines()
    register_re = r"Register [ABC]: (\d+)"
    ra = int(re.search(register_re, program_s[0]).groups()[0])
    rb = int(re.search(register_re, program_s[1]).groups()[0])
    rc = int(re.search(register_re, program_s[2]).groups()[0])
    instructions = list(map(int, program_s[-1].replace("Program: ", "").split(",")))
    return ra, rb, rc, instructions


def run_program(program: Program, output: list[int]):
    (ra, rb, rc, instructions), ip = program, 0
    while ip < len(instructions):
        opcode, operand = instructions[ip], instructions[ip + 1]

        match opcode:
            case 0:
                ra = ra // 2 ** get_combo_operand(operand, ra, rb, rc)
            case 1:
                rb = xor(rb, operand)
            case 2:
                rb = get_combo_operand(operand, ra, rb, rc) % 8
            case 3:
                if ra != 0:
                    ip = operand
                    continue
            case 4:
                rb = xor(rb, rc)
            case 5:
                output.append(get_combo_operand(operand, ra, rb, rc) % 8)
            case 6:
                rb = ra // 2 ** get_combo_operand(operand, ra, rb, rc)
            case 7:
                rc = ra // 2 ** get_combo_operand(operand, ra, rb, rc)
        ip += 2


def get_combo_operand(operand: int, ra: int, rb: int, rc: int):
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return ra
        case 5:
            return rb
        case 6:
            return rc
        case 7:
            raise ValueError("7 is not a valid combo operand")


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
