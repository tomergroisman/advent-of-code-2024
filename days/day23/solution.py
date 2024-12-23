import sys
from pathlib import Path
import networkx as nx


def part_1(raw_input: str) -> float:
    g = parse_input(raw_input)
    t_nodes = [node for node in g.nodes if node.startswith("t")]
    return sum([bool(set(cycle) & set(t_nodes)) for cycle in nx.simple_cycles(g, 3)])


def part_2(raw_input: str) -> str:
    g = parse_input(raw_input)
    clique = sorted(nx.find_cliques(g), key=len)[-1]
    return ",".join(sorted(clique))


def parse_input(raw_input: str):
    g = nx.Graph()
    for connection in raw_input.splitlines():
        a, b = connection.split("-")
        g.add_nodes_from([a, b])
        g.add_edge(a, b)
    return g


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
