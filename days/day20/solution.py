import sys
from pathlib import Path

type Maze = list[list[str]]
type Position = tuple[int, int]


def part_1(raw_input: str) -> float:
    maze, s, e = parse_input(raw_input)
    picos_from_s = set_picos_from_s(maze, s, e)
    saves = race(maze, s, picos_from_s, 2)
    return sum([n_saves for save, n_saves in saves.items() if save >= 100])


def part_2(raw_input: str) -> float:
    maze, s, e = parse_input(raw_input)
    picos_from_s = set_picos_from_s(maze, s, e)
    saves = race(maze, s, picos_from_s, 20)
    return sum([n_saves for save, n_saves in saves.items() if save >= 100])


def parse_input(raw_input: str) -> tuple[Maze, Position, Position]:
    maze = [list(row) for row in raw_input.splitlines()]
    s, e = (-1, -1), (-1, -1)
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == "S":
                s = (i, j)
            if maze[i][j] == "E":
                e = (i, j)
    return maze, s, e


def set_picos_from_s(
    maze: Maze,
    s: Position,
    e: Position,
):
    q, v, picos_from_s = [(s, 0)], set(), {}

    while q:
        p, steps = q.pop(0)
        picos_from_s[p] = steps
        if p == e:
            return picos_from_s

        if p in v:
            continue
        v.add(p)

        for d in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            np = (p[0] + d[0], p[1] + d[1])
            if (
                np not in v
                and 0 <= np[0] < len(maze)
                and 0 <= np[1] < len(maze[0])
                and maze[np[0]][np[1]] != "#"
            ):
                q.append((np, steps + 1))


def race(maze: Maze, s: Position, picos_from_s: dict[Position, int], cheat_length: int):
    q, v, cheats_save = [(s, 0, False)], set(), {}

    while q:
        (p, picos, has_cheat) = q.pop(0)

        if has_cheat:
            save = picos_from_s.get(p, 0) - picos
            if save > 0:
                cheats_save[save] = cheats_save.get(save, 0) + 1
            continue

        if p in v:
            continue
        v.add(p)

        cheat(maze, p, picos, q, cheat_length)

        for d in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            n_p = (p[0] + d[0], p[1] + d[1])
            if (
                0 <= n_p[0] < len(maze)
                and 0 <= n_p[1] < len(maze[0])
                and maze[n_p[0]][n_p[1]] != "#"
            ):
                q.append((n_p, picos + 1, False))

    return cheats_save


def cheat(maze: Maze, p: Position, picos: int, q: list, cheat_length: int):
    cheat_q, cheat_v, cheat_submit = [(p, (0, 0), 0)], set(), set()
    while cheat_q:
        c_p, c_d, size = cheat_q.pop(0)

        if size == cheat_length:
            break

        if (c_p, c_d) in cheat_v:
            continue
        cheat_v.add((c_p, c_d))

        for d in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            n_p = (c_p[0] + d[0], c_p[1] + d[1])
            if 0 <= n_p[0] < len(maze) and 0 <= n_p[1] < len(maze[0]):
                if maze[n_p[0]][n_p[1]] != "#" and n_p not in cheat_submit:
                    q.append((n_p, picos + size + 1, True))
                    cheat_submit.add(n_p)
                cheat_q.append((n_p, d, size + 1))


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
