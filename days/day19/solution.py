import sys
from pathlib import Path

type Patterns = dict[str, list[str]]
type Designs = list[str]


def part_1(raw_input: str) -> float:
    patterns, designs = parse_input(raw_input)
    return sum(get_is_designs_possible(patterns, designs))


def part_2(raw_input: str) -> float:
    patterns, designs = parse_input(raw_input)
    return sum(get_possible_designs(patterns, designs))


def parse_input(raw_input: str) -> tuple[Patterns, Designs]:
    patterns_s, designs_s = raw_input.split("\n\n")
    patterns = {}
    for pattern in patterns_s.split(", "):
        patterns[pattern[0]] = patterns.get(pattern[0], []) + [pattern]
    return patterns, designs_s.splitlines()


def get_is_designs_possible(patterns: Patterns, designs: Designs):
    return [
        get_n_possibilities_to_create_design(patterns, design) > 0 for design in designs
    ]


def get_possible_designs(patterns: Patterns, designs: Designs):
    return [
        get_n_possibilities_to_create_design(patterns, design) for design in designs
    ]


def get_n_possibilities_to_create_design(patterns: Patterns, design: str):
    memo = [0] * (len(design) + 1)
    memo[0] = 1

    for i in range(len(design)):
        relevant_patterns = patterns.get(design[i], [])
        for pattern in relevant_patterns:
            pattern_i = design[i:].find(pattern)
            if pattern_i == 0:
                memo[i + len(pattern)] += memo[i]

    return memo[len(design)]


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
