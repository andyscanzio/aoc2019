from intcode import Intcode
from util import load_inputs

_, input = load_inputs("11", has_test=False)


def part1(data: str) -> int:
    grid: dict[complex, int] = {}
    info = {"dir": 1j, "pos": 0j}
    painted: set[complex] = set()
    out: list[int] = []

    def input() -> int:
        if info["pos"] not in grid:
            return 0
        return grid[info["pos"]]

    def output(x: int) -> None:
        out.append(x)
        if len(out) == 2:
            paint, turn = out
            grid[info["pos"]] = paint
            painted.add(info["pos"])
            info["dir"] = info["dir"] * (1j if turn == 0 else -1j)
            info["pos"] += info["dir"]
            out.clear()

    Intcode(data, input, output).run()
    return len(painted)


def part2(data: str) -> str:
    grid: dict[complex, int] = {0j: 1}
    info = {"dir": 1j, "pos": 0j}
    painted: set[complex] = set()
    out: list[int] = []

    def input() -> int:
        if info["pos"] not in grid:
            return 0
        return grid[info["pos"]]

    def output(x: int) -> None:
        out.append(x)
        if len(out) == 2:
            paint, turn = out
            grid[info["pos"]] = paint
            painted.add(info["pos"])
            info["dir"] = info["dir"] * (1j if turn == 0 else -1j)
            info["pos"] += info["dir"]
            out.clear()

    Intcode(data, input, output).run()
    minx = int(min(key.real for key in grid.keys()))
    maxx = int(max(key.real for key in grid.keys()))
    miny = int(min(key.imag for key in grid.keys()))
    maxy = int(max(key.imag for key in grid.keys()))

    return "\n".join(
        "".join(
            ("X" if grid[x + 1j * y] == 1 else " ") if x + 1j * y in grid else " "
            for x in range(minx, maxx + 1)
        )
        for y in range(maxy, miny - 1, -1)
    )


print(part1(input))
print(part2(input))
