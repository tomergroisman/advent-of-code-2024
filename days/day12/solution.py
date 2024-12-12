import sys
from pathlib import Path


def part_1(raw_input: str) -> float:
    mx = parse_input(raw_input)
    return get_fence_price(mx, False)


def part_2(raw_input: str) -> float:
    mx = parse_input(raw_input)
    return get_fence_price(mx, True)


def parse_input(raw_input: str) -> list[list[str]]:
    return [list(row) for row in raw_input.splitlines()]


def get_fence_price(mx: list[list[str]], count_sides: bool):
    areas_and_perimeters, v = [], set()
    for i in range(len(mx)):
        for j in range(len(mx[0])):
            area_and_perimeter = get_area_and_perimeter(mx, i, j, v)
            if area_and_perimeter is not None:
                areas_and_perimeters.append(area_and_perimeter)
    return sum([a * (s if count_sides else p) for (a, p, s) in areas_and_perimeters])


def get_area_and_perimeter(
    mx: list[list[str]],
    i: int,
    j: int,
    v: set[tuple[int, int]],
):
    if (i, j) in v:
        return None

    plant, q = mx[i][j], [(i, j)]
    a, p, s = 0, 0, 0
    n, m = len(mx), len(mx[0])

    while q:
        (pi, pj) = q.pop()

        if (pi, pj) in v:
            continue

        a += 1
        for d in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            ni, nj = pi + d[0], pj + d[1]
            if 0 <= ni < n and 0 <= nj < m and mx[ni][nj] == plant:
                q.append((ni, nj))
            else:
                p += 1

        for d in [
            ((-1, 0), (0, 1), (-1, 1)),
            ((0, 1), (1, 0), (1, 1)),
            ((1, 0), (0, -1), (1, -1)),
            ((0, -1), (-1, 0), (-1, -1)),
        ]:
            n1, n2, n3 = (
                (pi + d[0][0], pj + d[0][1]),
                (pi + d[1][0], pj + d[1][1]),
                (pi + d[2][0], pj + d[2][1]),
            )
            is_n1_sibling = (
                0 <= n1[0] < n and 0 <= n1[1] < m and mx[n1[0]][n1[1]] == plant
            )
            is_n2_sibling = (
                0 <= n2[0] < n and 0 <= n2[1] < m and mx[n2[0]][n2[1]] == plant
            )
            is_n3_sibling = (
                0 <= n3[0] < n and 0 <= n3[1] < m and mx[n3[0]][n3[1]] == plant
            )
            is_inner = is_n1_sibling and is_n2_sibling and not is_n3_sibling
            is_outer = not is_n1_sibling and not is_n2_sibling
            if is_inner or is_outer:
                s += 1

        v.add((pi, pj))

    return a, p, s


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
