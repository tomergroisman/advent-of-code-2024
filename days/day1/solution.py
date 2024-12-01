import sys
from pathlib import Path
import bisect


def part_1(raw_input: str) -> float:
    location_ids_1, location_ids_2 = parse_input(raw_input)
    return sum(
        [abs(location_ids_1[i] - location_ids_2[i]) for i in range(len(location_ids_1))]
    )


def part_2(raw_input: str) -> float:
    location_ids_1, location_ids_2 = parse_input(raw_input)
    location_ids_2_appearances_by_location_id = get_appearances_by_location_id(
        location_ids_2
    )
    return sum(
        [
            location_id * location_ids_2_appearances_by_location_id.get(location_id, 0)
            for location_id in location_ids_1
        ]
    )


def get_appearances_by_location_id(location_ids: list[int]) -> dict[int, int]:
    appearances = {}
    for location_id in location_ids:
        appearances[location_id] = appearances.get(location_id, 0) + 1
    return appearances


def parse_input(raw_input: str) -> tuple[list[int], list[int]]:
    location_ids_1, location_ids_2 = [], []
    for location_id_1, location_id_2 in [
        row.split("   ") for row in raw_input.splitlines()
    ]:
        bisect.insort(location_ids_1, int(location_id_1))
        bisect.insort(location_ids_2, int(location_id_2))
    return location_ids_1, location_ids_2


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
