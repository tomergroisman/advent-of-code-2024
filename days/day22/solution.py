import sys
from functools import cache
from operator import xor
from pathlib import Path


def part_1(raw_input: str) -> float:
    initial_secrets, s = parse_input(raw_input), 0
    for secret in initial_secrets:
        for i in range(2000):
            secret = next_secret(secret)
        s += secret
    return s


def part_2(raw_input: str) -> float:
    initial_secrets, s = parse_input(raw_input), 0
    price_maps = generate_price_maps(initial_secrets)
    sequences = generate_valid_sequences()
    values_by_sequence: dict[tuple[int, ...], list[int]] = {}
    for sequence in sequences:
        values_by_sequence[sequence] = []
        for i, price_map in enumerate(price_maps):
            value = price_map.get(sequence, 0)
            values_by_sequence[sequence].append(value)
        values_by_sequence[sequence] = [sum(values_by_sequence[sequence])]
    return max([n[0] for n in values_by_sequence.values()])


def parse_input(raw_input: str) -> list[int]:
    return [int(n_str) for n_str in raw_input.splitlines()]


@cache
def next_secret(n: int):
    s1 = prune(mix(n, 64 * n))
    s2 = prune(mix(s1, s1 // 32))
    return prune(mix(s2, s2 * 2048))


def mix(secret: int, other: int):
    return xor(secret, other)


def prune(secret: int):
    return secret % 16777216


def generate_valid_sequences():
    sequences = []
    for x1 in range(-9, 10, 1):
        for x2 in range(-9, 10, 1):
            if abs(x1 - x2) >= 10:
                continue
            for x3 in range(-9, 10, 1):
                if abs(x2 - x3) >= 10 or abs(x1 - x2 - x3) >= 10:
                    continue
                for x4 in range(-9, 10, 1):
                    if abs(x2 - x3 - x4) >= 10 or abs(x3 - x4) >= 10:
                        continue
                    if 0 <= x1 + x2 + x3 + x4 < 10:
                        sequences.append((x1, x2, x3, x4))
    return sequences


def generate_price_maps(initial_secrets: list[int]):
    changes: list[list[int | None]] = []
    prices: list[list[int]] = []
    price_maps: list[dict[tuple[int, ...], int]] = []
    for i, secret in enumerate(initial_secrets):
        changes.append([None])
        prices.append([secret % 10])
        price_maps.append({})
        prev, current = None, secret
        for j in range(2000):
            current = next_secret(current)
            last_digit = current % 10
            prices[i].append(last_digit)
            if prev is None:
                changes[i].append(last_digit - secret % 10)
            else:
                changes[i].append(last_digit - prev % 10)
            prev = current
            if j >= 4:
                if price_maps[i].get(tuple(changes[i][j - 3 : j + 1])) is not None:
                    continue
                price_maps[i][tuple(changes[i][j - 3 : j + 1])] = prices[i][j]
        changes[i] = changes[i][:-1]
    return price_maps


input_filename = sys.argv[1]
part = sys.argv[2]
current_input = open(Path(__file__).parent.joinpath(input_filename)).read()
match part:
    case "1":
        print(part_1(current_input))
    case "2":
        print(part_2(current_input))
