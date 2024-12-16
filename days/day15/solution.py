import sys
from pathlib import Path

type Board = list[list[str]]
type Movements = str
type Position = tuple[int, int]
type Delta = tuple[int, int]


def part_1(raw_input: str) -> float:
    board, movements = parse_input(raw_input, False)
    run_robot(board, movements)
    return calc_gps(board)


def part_2(raw_input: str) -> float:
    board, movements = parse_input(raw_input, True)
    run_robot(board, movements)
    return calc_gps(board)


def parse_input(raw_input: str, extended: bool) -> tuple[Board, Movements]:
    board_s, movements = raw_input.split("\n\n")
    board = [list(row) for row in board_s.splitlines()]
    extended_board = []
    for i in range(len(board)):
        extended_board.append([])
        for j in range(len(board[0])):
            if board[i][j] == "@":
                extended_board[i].extend(["@", "."])
            elif board[i][j] == "O":
                extended_board[i].extend(["[", "]"])
            else:
                extended_board[i].extend([board[i][j]] * 2)
    return extended_board if extended else board, movements


def run_robot(board: Board, movements: Movements):
    p = get_robot_position(board)
    for movement in movements:
        match movement:
            case "^":
                p = move_object(board, p, (-1, 0))
            case ">":
                p = move_object(board, p, (0, 1))
            case "v":
                p = move_object(board, p, (1, 0))
            case "<":
                p = move_object(board, p, (0, -1))


def move_object(board: Board, p: Position, d: Delta) -> Position:
    pn = p[0] + d[0], p[1] + d[1]
    c = board[pn[0]][pn[1]]

    match c:
        case ".":
            advance(board, p, pn)
            return pn
        case "#":
            is_blocked = True
            return p
        case "O":
            if move_object(board, pn, d) == pn:
                return p
            else:
                advance(board, p, pn)
                return pn
        case "[" | "]":
            if d[0] == 0:
                if move_object(board, pn, d) == pn:
                    return p
                else:
                    advance(board, p, pn)
                    return pn
            else:
                if is_end_blocked(board, p, d):
                    return p

                pnn = (pn[0], pn[1] + 1) if c == "[" else (pn[0], pn[1] - 1)
                m1, m2 = move_object(board, pn, d), move_object(board, pnn, d)

                if m1 == pn and m2 == pnn:
                    return p
                elif m1 != pn and m2 != pnn:
                    advance(board, p, pn)
                    return pn
                else:
                    if m1 != pn:
                        revert(board, m1, pn)
                        return p
                    if m2 != pnn:
                        revert(board, m2, pnn)
                        return p


def is_end_blocked(board: Board, p: Position, d: Delta):
    q, v = [p], set()

    while q:
        p = q.pop(0)

        if p in v:
            continue
        v.add(p)

        c = board[p[0]][p[1]]

        if c == "#":
            return True

        if c == "[":
            q.append((p[0], p[1] + 1))
            q.append((p[0] + d[0], p[1] + d[1]))
        elif c == "]":
            q.append((p[0], p[1] - 1))
            q.append((p[0] + d[0], p[1] + d[1]))

    return False


def advance(board: Board, a: Position, b: Position):
    a_i, a_j = a
    b_i, b_j = b
    board[b_i][b_j], board[a_i][a_j] = board[a_i][a_j], board[b_i][b_j]


def revert(board: Board, a: Position, b: Position):
    a_i, a_j = a
    b_i, b_j = b
    board[a_i][a_j], board[b_i][b_j] = board[b_i][b_j], board[a_i][a_j]


def get_robot_position(board: Board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == "@":
                return i, j


def calc_gps(board: Board):
    res = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == "O" or board[i][j] == "[":
                res += 100 * i + j
    return res


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
