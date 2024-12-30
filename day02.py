from intcode import Intcode
from util import load_inputs

test, input = load_inputs("2")


def part1(data: str) -> int:
    return Intcode(data).set_value(1, 12).set_value(2, 2).run()


def part2(data: str) -> int:
    for noun in range(117):
        for verb in range(117):
            if Intcode(data).set_value(1, noun).set_value(2, verb).run() == 19690720:
                return 100 * noun + verb
    return 0


print(part1(input))
print(part2(input))
