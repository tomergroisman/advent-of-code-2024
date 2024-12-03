import sys
from pathlib import Path


def part_1(raw_input: str) -> float:
    reports = parse_input(raw_input)
    return sum([is_safe_report(report, False) for report in reports])


def part_2(raw_input: str) -> float:
    reports = parse_input(raw_input)
    return sum([is_safe_report(report, True) for report in reports])


def is_safe_report(report: list[int], should_tolerate: bool):
    prev = report[0]
    current = report[1]
    if prev == current:
        return handle_unsafe_report(report, should_tolerate)
    is_increasing = prev < current

    for current in report[1:]:
        diff = abs(current - prev)
        if diff < 1 or diff > 3:
            return handle_unsafe_report(report, should_tolerate)
        if is_increasing and prev > current:
            return handle_unsafe_report(report, should_tolerate)
        if not is_increasing and prev < current:
            return handle_unsafe_report(report, should_tolerate)
        prev = current
    return True


def handle_unsafe_report(report: list[int], should_tolerate: bool):
    if should_tolerate:
        for i in range(len(report)):
            attempt = report.copy()
            attempt.pop(i)
            if is_safe_report(attempt, False):
                return True
    return False


def parse_input(raw_input: str) -> list[list[int]]:
    return [list(map(int, report.split(" "))) for report in raw_input.splitlines()]


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
