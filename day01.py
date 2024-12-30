from util import load_inputs

test, input = load_inputs("1")


def part1(data: str) -> int:
    return sum(int(i) // 3 - 2 for i in data.splitlines())


def fuel(mass: int) -> int:
    c = -mass
    while mass > 0:
        c += mass
        mass = mass // 3 - 2
    return c


def part2(data: str) -> int:
    return sum(map(fuel, map(int, data.splitlines())))


print(part1(input))
print(part2(input))
