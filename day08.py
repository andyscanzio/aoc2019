from util import load_inputs
from itertools import batched

test, input = load_inputs("8")


def part1(data: str, width: int, height: int) -> int:
    layers = list(batched(data, width * height))
    layer = min(range(len(layers)), key=lambda x: layers[x].count("0"))
    return layers[layer].count("1") * layers[layer].count("2")


def part2(data: str, width: int, height: int) -> str:
    layers = list(batched(data, width * height))
    res: list[str] = []
    for i in range(width * height):
        p = ""
        l = 0
        while p not in ("0", "1"):
            p = layers[l][i]
            l += 1
        res.append(p)
    return "\n".join(
        "".join("X" if i == "1" else " " for i in line) for line in batched(res, width)
    )


print(part1(input, 25, 6))
print(part2(input, 25, 6))
