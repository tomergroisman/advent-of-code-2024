import sys
from pathlib import Path

type Map = list[list[int]]
type Point = tuple[int, int]


def part_1(raw_input: str) -> float:
    mx = parse_input(raw_input)
    return get_trailheads_score(mx, False)


def part_2(raw_input: str) -> float:
    mx = parse_input(raw_input)
    return get_trailheads_score(mx, True)


def parse_input(raw_input: str) -> Map:
    return [[int(n) for n in row] for row in raw_input.splitlines()]


def get_trailheads_score(mx: Map, is_rating: bool) -> int:
    trailheads_score = 0
    for i in range(len(mx)):
        for j in range(len(mx[0])):
            if mx[i][j] == 0:
                trailheads_score += get_single_trailhead_score(mx, i, j, is_rating)
    return trailheads_score


def get_single_trailhead_score(mx: Map, i: int, j: int, is_rating: bool) -> int:
    q, v, score = [(i, j)], set(), 0
    while q:
        (pi, pj) = q.pop(0)

        h = mx[pi][pj]
        if h == 9:
            if not is_rating and (pi, pj) in v:
                continue
            v.add((pi, pj)),
            score += 1
            continue

        for d in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            next_p = (pi + d[0], pj + d[1])
            is_valid_point = 0 <= next_p[0] < len(mx) and 0 <= next_p[1] < len(mx[0])
            if is_valid_point:
                next_h = mx[next_p[0]][next_p[1]]
                is_valid_trail = next_h - h == 1
                if is_valid_trail:
                    q.append(next_p)
    return score


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
