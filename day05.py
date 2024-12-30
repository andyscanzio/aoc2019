from intcode import Intcode
from util import load_inputs
from typing import Callable

test, input = load_inputs("5")


def part1(data: str) -> int:
    input: Callable[[], int] = lambda: 1
    output: Callable[[int], None] = lambda x: print(x)
    return Intcode(data, input, output).run()


def part2(data: str) -> int:
    input: Callable[[], int] = lambda: 5
    output: Callable[[int], None] = lambda x: print(x)
    return Intcode(data, input, output).run()


part1(input)
part2(input)
