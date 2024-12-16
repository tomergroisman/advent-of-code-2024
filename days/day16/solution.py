import sys
from copy import deepcopy
from pathlib import Path
import heapq
from math import inf

type Maze = list[list[str]]


def part_1(raw_input: str) -> float:
    maze = parse_input(raw_input)
    return find_lowest_score(maze)[0]


def part_2(raw_input: str) -> float:
    maze = parse_input(raw_input)
    return find_lowest_score(maze)[1]


def parse_input(raw_input: str) -> Maze:
    return [list(row) for row in raw_input.splitlines()]


def find_lowest_score(maze: Maze):
    s = len(maze) - 2, 1
    min_heap, v = [(0, s, (0, 1), set())], dict()
    best_seats, best_score = set(), inf

    while min_heap:
        score, p, d, path = heapq.heappop(min_heap)
        if score > best_score:
            break

        if (p, d) in v and v[(p, d)] < score:
            continue

        v[(p, d)] = score
        n_path = path.copy()
        n_path.add(p)

        if maze[p[0]][p[1]] == "E":
            best_score = score
            best_seats.update(list(n_path))

        for n_d in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            is_valid_rotation = abs(d[0]) != abs(n_d[0])
            if is_valid_rotation:
                heapq.heappush(min_heap, (score + 1000, p, n_d, n_path))
            else:
                is_same_direction = d == n_d
                if is_same_direction:
                    n_p = p[0] + n_d[0], p[1] + n_d[1]
                    is_valid_step = maze[n_p[0]][n_p[1]] != "#"
                    if is_valid_step:
                        heapq.heappush(min_heap, (score + 1, n_p, d, n_path))

    return best_score, len(best_seats)


def print_maze(maze: Maze):
    print("\n".join(["".join(["{:1}".format(item) for item in row]) for row in maze]))


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
