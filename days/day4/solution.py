import sys
from pathlib import Path


def part_1(raw_input: str) -> float:
    mx = parse_input(raw_input)
    hits = 0
    for i in range(len(mx)):
        for j, c in enumerate(mx[i]):
            hits += get_xmas_hits(c, mx, (i, j), False)
    return hits


def part_2(raw_input: str) -> float:
    mx = parse_input(raw_input)
    hits = 0
    for i in range(len(mx)):
        for j, c in enumerate(mx[i]):
            hits += get_xmas_hits(c, mx, (i, j), True)
    return hits


def parse_input(raw_input: str) -> list[list[str]]:
    return [list(row) for row in raw_input.splitlines()]


def get_xmas_hits(
    c: str, mx: list[list[str]], position: tuple[int, int], scissors: bool
):
    opts = []
    i, j = position
    n, m = len(mx), len(mx[0])

    if not scissors and c == "X":
        if j <= m - 4:
            opts.append("".join([mx[i][j + k] for k in range(4)]))
        if j >= 3:
            opts.append("".join([mx[i][j - k] for k in range(4)]))
        if i <= n - 4:
            opts.append("".join([mx[i + k][j] for k in range(4)]))
        if i >= 3:
            opts.append("".join([mx[i - k][j] for k in range(4)]))
        if i <= n - 4 and j <= m - 4:
            opts.append("".join([mx[i + k][j + k] for k in range(4)]))
        if i >= 3 and j <= m - 4:
            opts.append("".join([mx[i - k][j + k] for k in range(4)]))
        if i <= n - 4 and j >= 3:
            opts.append("".join([mx[i + k][j - k] for k in range(4)]))
        if i >= 3 and j >= 3:
            opts.append("".join([mx[i - k][j - k] for k in range(4)]))
        return len([w for w in opts if w == "XMAS"])

    if scissors and c == "A" and 0 < i < n - 1 and 0 < j < m - 1:
        opts.append("".join([mx[i - 1 + k][j - 1 + k] for k in range(3)])),
        opts.append("".join([mx[i + 1 - k][j - 1 + k] for k in range(3)])),
        opts.append("".join([mx[i - 1 + k][j + 1 - k] for k in range(3)])),
        opts.append("".join([mx[i + 1 - k][j + 1 - k] for k in range(3)])),
        return 1 if len([w for w in opts if w == "MAS"]) == 2 else 0

    return 0


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
