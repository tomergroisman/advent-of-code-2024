import sys
from pathlib import Path


def part_1(raw_input: str) -> float:
    stones, n = parse_input(raw_input), 25
    res = 0
    for stone in stones:
        res += stone_transform(stone, 0, {}, n)
    return res


def part_2(raw_input: str) -> float:
    stones, n = parse_input(raw_input), 75
    res = 0
    for stone in stones:
        res += stone_transform(stone, 0, {}, n)
    return res


def parse_input(raw_input: str) -> list[int]:
    return list(map(int, raw_input.splitlines()[0].split(" ")))


def stone_transform(stone: int, i_count: int, st_states: dict, n: int) -> int:
    stone_count = 1

    if i_count == n:
        st_states[stone, i_count] = stone_count
        return 1

    if (stone, i_count) in st_states:
        return st_states[(stone, i_count)]

    if stone == 0:
        stone_count = stone_transform(1, i_count + 1, st_states, n)
    elif len(str(stone)) % 2 == 0:
        first = int(str(stone)[0 : len(str(stone)) // 2])
        second = int(str(stone)[len(str(stone)) // 2 :])
        stone_count = stone_transform(
            first, i_count + 1, st_states, n
        ) + stone_transform(second, i_count + 1, st_states, n)
    else:
        stone_count = stone_transform(stone * 2024, i_count + 1, st_states, n)

    st_states[stone, i_count] = stone_count
    return stone_count


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
