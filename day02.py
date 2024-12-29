from intcode import Intcode
from util import load_inputs
from itertools import batched

test, input = load_inputs("2")


def part1(data: str) -> None:
    Intcode(data).set_value(1, 12).set_value(2, 2).run()


def part2(data: str) -> None:
    for noun in range(117):
        for verb in range(117):
            if (
                Intcode(data).set_value(1, noun).set_value(2, verb).run(True)
                == 19690720
            ):
                print(100 * noun + verb)


part1(input)
part2(input)
