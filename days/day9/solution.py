import sys
from pathlib import Path

type MemoryData = tuple[int, int]


def part_1(raw_input: str) -> float:
    disk_map = parse_input(raw_input)
    order_free_space(disk_map)
    return calc_checksum(disk_map)


def part_2(raw_input: str) -> float:
    disk_map = parse_input(raw_input)
    order_free_space_blocks(disk_map)
    # print(disk_map)
    return calc_checksum(disk_map)


def parse_input(raw_input: str) -> list[MemoryData]:
    return [
        (i // 2 if i % 2 == 0 else -1, int(data))
        for i, data in enumerate(list(raw_input.strip()))
    ]


def swap(
    disk_map: list[MemoryData],
    free_space_idx: int,
    full_space_idx: int,
    local_swap: bool,
):
    free_space, full_space = disk_map[free_space_idx], disk_map[full_space_idx]
    is_full_contained = full_space[1] < free_space[1]
    is_full_overflow = full_space[1] > free_space[1]
    if is_full_contained:
        disk_map[free_space_idx] = (free_space[0], free_space[1] - full_space[1])
        disk_map.pop(full_space_idx)
        disk_map.insert(free_space_idx, full_space)
        if local_swap:
            disk_map.insert(full_space_idx, (free_space[0], full_space[1]))
        else:
            disk_map.append((free_space[0], full_space[1]))
        return free_space_idx + 1, full_space_idx - 1
    elif is_full_overflow:
        disk_map.append(free_space)
        disk_map[full_space_idx] = (full_space[0], full_space[1] - free_space[1])
        disk_map[free_space_idx] = (full_space[0], free_space[1])
        return free_space_idx + 2, full_space_idx
    else:
        disk_map[free_space_idx], disk_map[full_space_idx] = (
            disk_map[full_space_idx],
            disk_map[free_space_idx],
        )
        return free_space_idx + 2, full_space_idx - 2


def order_free_space(disk_map: list[MemoryData]):
    current_free_idx = 1
    current_full_idx = len(disk_map) - 1
    while current_free_idx < current_full_idx:
        current_free_idx, current_full_idx = swap(
            disk_map, current_free_idx, current_full_idx, False
        )


def order_free_space_blocks(disk_map: list[MemoryData]):
    visited = set()
    current_full_idx = len(disk_map) - 1
    while current_full_idx is not None:
        visited.add(disk_map[current_full_idx][0])
        full_space = disk_map[current_full_idx]
        free_space_idx = next(
            (
                free_space_idx
                for free_space_idx, data in enumerate(disk_map[:current_full_idx])
                if (data[0] == -1 and full_space[1] <= data[1])
            ),
            None,
        )
        if free_space_idx is not None:
            swap(disk_map, free_space_idx, current_full_idx, True)

        current_full_idx = next(
            (
                len(disk_map) - 1 - i
                for i, data in enumerate(disk_map[::-1])
                if data[0] != -1 and not data[0] in visited
            ),
            None,
        )


def calc_checksum(disk_map: list[MemoryData]):
    res, current_idx = 0, 0
    for memory_data in disk_map:
        for block in range(memory_data[1]):
            if memory_data[0] != -1:
                res += memory_data[0] * current_idx
            current_idx += 1
    return res


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
