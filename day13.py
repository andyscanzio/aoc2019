from util import load_inputs
from intcode import Intcode
from itertools import batched

_, input = load_inputs("13", has_test=False)


def part1(data: str) -> int:
    output = Intcode(data).run()
    return sum(id == 2 for _, _, id in batched(output, 3))


def part2(data: str) -> int:
    info = {"ball": 0, "pad": 0, "score": 0}
    out: list[int] = []

    def input() -> int:
        ball = info["ball"]
        pad = info["pad"]
        if pad < ball:
            return 1
        if pad > ball:
            return -1
        return 0

    def output(o: int) -> None:
        out.append(o)
        if len(out) == 3:
            x, y, id = out
            if x == -1 and y == 0:
                info["score"] = id
            elif id == 3:
                info["pad"] = x
            elif id == 4:
                info["ball"] = x
            out.clear()

    Intcode(data, input, output).set_value(0, 2).run()
    return info["score"]


print(part1(input))
print(part2(input))
