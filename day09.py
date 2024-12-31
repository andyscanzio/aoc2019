from intcode import Intcode
from util import load_inputs

test, input = load_inputs("9")


def part1(data: str) -> int:
    return Intcode(data, lambda: 1).run()[0]


def part2(data: str) -> int:
    return Intcode(data, lambda: 2).run()[0]


print(part1(input))
print(part2(input))
