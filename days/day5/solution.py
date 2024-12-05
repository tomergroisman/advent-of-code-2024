import sys
from pathlib import Path


def part_1(raw_input: str) -> float:
    before_by_number, updates = parse_input(raw_input)
    valid_updates = [
        update for update in updates if is_valid_update(update, before_by_number)
    ]
    mid_numbers = [
        valid_update[len(valid_update) // 2] for valid_update in valid_updates
    ]
    return sum(mid_numbers)


def part_2(raw_input: str) -> float:
    before_by_number, updates = parse_input(raw_input)
    invalid_updates = [
        update for update in updates if not is_valid_update(update, before_by_number)
    ]
    fixed_invalid_updates = [
        fix_invalid_update(invalid_update, before_by_number)
        for invalid_update in invalid_updates
    ]
    mid_numbers = [
        valid_update[len(valid_update) // 2] for valid_update in fixed_invalid_updates
    ]
    return sum(mid_numbers)


def parse_input(raw_input: str) -> tuple[dict[int, list[int]], list[list[int]]]:
    lines = raw_input.splitlines()
    separator_index = lines.index("")
    orders, updates_s = lines[:separator_index], lines[separator_index + 1 :]
    updates = [list(map(int, s.split(","))) for s in updates_s]
    before_by_number = {}
    for order in orders:
        pre, post = list(map(int, order.split("|")))
        before = before_by_number.get(pre, [])
        before.append(post)
        before_by_number[pre] = before
    return before_by_number, updates


def is_valid_update(update: list[int], before_by_number: dict[int, list[int]]) -> bool:
    visited = []
    for n in update:
        before_numbers = before_by_number.get(n, [])
        if list(set(before_numbers) & set(visited)):
            return False
        visited.append(n)
    return True


def fix_invalid_update(update: list[int], before_by_number: dict[int, list[int]]):
    while not is_valid_update(update, before_by_number):
        visited = []
        for i, n in enumerate(update):
            before_numbers = before_by_number.get(n, [])
            if list(set(before_numbers) & set(visited)):
                update[i], update[i - 1] = update[i - 1], update[i]
                continue
            visited.append(n)
    return update


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
