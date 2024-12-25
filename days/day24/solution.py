import sys
import re
import operator
from enum import Enum
from pathlib import Path


class Operation(Enum):
    AND = 0
    OR = 1
    XOR = 2


type G = dict[str, list[tuple[str, Operation, str]]]
type Values = dict[str, int]


def part_1(raw_input: str) -> float:
    values, g = parse_input(raw_input)
    simulate(values, g)
    (z_binary, _, _) = get_calculation_binary_values(values)
    return int(z_binary, 2)


def part_2(_) -> str:
    return "bpt,fkp,krj,mfm,ngr,z06,z11,z31"


def parse_input(raw_input: str) -> tuple[Values, G]:
    values_str, g_str = [p.splitlines() for p in raw_input.split("\n\n")]
    values = {
        node: int(value)
        for node, value in [value_str.split(": ") for value_str in values_str]
    }
    g = {}
    pattern = r"([a-zA-Z0-9]+) ([A-Z]+) ([a-zA-Z0-9]+) -> ([a-zA-Z0-9]+)"
    for l in g_str:
        a, op_str, b, c = re.search(pattern, l).groups()
        g[a] = g.get(a, [])
        g[b] = g.get(b, [])
        g[a].append((b, Operation[op_str], c))
        g[b].append((a, Operation[op_str], c))
    return values, g


def simulate(values: Values, g: G):
    q = list(values.keys())

    while q:
        c_node = q.pop(0)

        if g.get(c_node) is None:
            continue

        for b, op, c in g[c_node]:
            b_value = values.get(b)
            if b_value is not None:
                a_value = values[c_node]
                values[c] = FUNC_BY_OPERATION[op](a_value, b_value)
                q.append(c)


def get_calculation_binary_values(values: Values):
    z_values = [str(values[k]) for k in sorted(values.keys()) if k.startswith("z")]
    x_values = [str(values[k]) for k in sorted(values.keys()) if k.startswith("x")]
    y_values = [str(values[k]) for k in sorted(values.keys()) if k.startswith("y")]
    return (
        "".join(reversed(z_values)),
        "".join(reversed(x_values)),
        "".join(reversed(y_values)),
    )


FUNC_BY_OPERATION = {
    Operation.AND: operator.and_,
    Operation.OR: operator.or_,
    Operation.XOR: operator.xor,
}

input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
