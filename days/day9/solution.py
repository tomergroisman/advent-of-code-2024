import sys
from pathlib import Path

type MemoryData = tuple[int | None, int]


def part_1(raw_input: str) -> float:
    disk_map = parse_input(raw_input)
    free_space(disk_map)
    return calc_checksum(disk_map)


def part_2(raw_input: str) -> float:
    disk_map = parse_input(raw_input)
    free_space_blocks(disk_map)
    return calc_checksum(disk_map)


def parse_input(raw_input: str) -> list[MemoryData]:
    return [
        (i // 2 if i % 2 == 0 else None, int(data))
        for i, data in enumerate(list(raw_input.strip()))
    ]


def free_space(disk_map: list[MemoryData]):
    free_i, file_i = 1, len(disk_map) - 1
    while free_i < file_i:
        free_block, file_block = disk_map[free_i], disk_map[file_i]
        will_be_contained = file_block[1] < free_block[1]
        will_fit = file_block[1] == free_block[1]
        if will_be_contained:
            disk_map[free_i] = (file_block[0], file_block[1])
            disk_map[file_i] = (None, file_block[1])
            disk_map.insert(free_i + 1, (None, free_block[1] - file_block[1]))
            file_i -= 1
            free_i += 1
        elif will_fit:
            disk_map[free_i], disk_map[file_i] = disk_map[file_i], disk_map[free_i]
            file_i -= 2
            free_i += 2
        else:
            disk_map[free_i] = (file_block[0], free_block[1])
            disk_map[file_i] = (file_block[0], file_block[1] - free_block[1])
            disk_map.insert(file_i + 1, (None, free_block[1]))
            free_i += 2


def free_space_blocks(disk_map: list[MemoryData]):
    file_i = len(disk_map) - 1
    while file_i > 0:
        file_block = disk_map[file_i]

        for i, block in enumerate(disk_map[:file_i]):
            if block[0] is not None:
                continue
            free_block, free_i = block, i
            will_be_contained = file_block[1] < free_block[1]
            will_fit = file_block[1] == free_block[1]
            if will_be_contained:
                disk_map[free_i] = (file_block[0], file_block[1])
                disk_map[file_i] = (None, file_block[1])
                disk_map.insert(free_i + 1, (None, free_block[1] - file_block[1]))
                break
            elif will_fit:
                disk_map[free_i], disk_map[file_i] = disk_map[file_i], disk_map[free_i]
                break

        file_i = file_i - 1 if disk_map[file_i - 1][0] is not None else file_i - 2


def calc_checksum(disk_map: list[MemoryData]):
    res, i = 0, 0
    for data in disk_map:
        for block in range(data[1]):
            res += i * (data[0] or 0)
            i += 1
    return res


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
