import heapq
import sys
from pathlib import Path

type Position = tuple[int, int]
type Board = list[list[str]]


def part_1(raw_input: str) -> float:
    falling_bytes, n_falling, n = parse_input(raw_input), 1024, 71
    board = generate_board(n)
    fall_bytes(board, falling_bytes, n_falling)
    return find_shortest_path(board, (0, 0), (n - 1, n - 1))


def part_2(raw_input: str) -> str:
    falling_bytes, n = parse_input(raw_input), 71
    board = generate_board(n)
    blocking_byte = find_blocking_byte(board, falling_bytes, n)
    return f"{blocking_byte[0]},{blocking_byte[1]}"


def parse_input(raw_input: str) -> list[Position]:
    return [tuple(map(int, row.split(","))) for row in raw_input.splitlines()]


def generate_board(n: int):
    return [["."] * n for _ in range(n)]


def fall_bytes(board: Board, falling_bytes: list[Position], n_falling: int):
    for i in range(n_falling):
        fall_byte(board, falling_bytes[i])


def fall_byte(board: Board, falling_byte: Position):
    (bj, bi) = falling_byte
    board[bi][bj] = "#"


def find_shortest_path(board: Board, s: Position, e: Position):
    q, v = [], set()
    heapq.heappush(q, (0, s))
    n, m = len(board), len(board[0])

    while q:
        steps, p = heapq.heappop(q)

        if p in v:
            continue

        if p == e:
            return steps

        v.add(p)
        for d in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            n_p = tuple(a + b for a, b in zip(p, d))
            n_pi, n_pj = n_p
            if 0 <= n_pi < n and 0 <= n_pj < m and board[n_pi][n_pj] == ".":
                heapq.heappush(q, (steps + 1, n_p))


def find_blocking_byte(board: Board, falling_bytes: list[Position], n: int):
    for i, falling_byte in enumerate(falling_bytes):
        fall_byte(board, falling_byte)
        if find_shortest_path(board, (0, 0), (n - 1, n - 1)) is None:
            return falling_byte


def print_board(board: Board):
    print("\n".join(["".join(["{:1}".format(item) for item in row]) for row in board]))


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
