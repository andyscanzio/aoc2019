from util import load_inputs

test, input = load_inputs("3")

dir: dict[str, complex] = {"U": 1j, "R": 1, "D": -1j, "L": -1}


def part1(data: str) -> int:
    sets: list[set[complex]] = []
    for wire in data.splitlines():
        pos = 0j
        w: set[complex] = set()
        for move in wire.split(","):
            d, q = move[0], int(move[1:])
            for _ in range(q):
                pos += dir[d]
                w.add(pos)
        sets.append(w)
    inte: set[complex] | None = None
    for s in sets:
        if inte is None:
            inte = s
        else:
            inte.intersection_update(s)
    assert inte is not None
    return min(list(map(lambda x: int(abs(x.real) + abs(x.imag)), inte)))


def part2(data: str) -> int:
    def get_steps(wire: str) -> dict[complex, int]:
        pos = 0j
        c = 0
        visited: dict[complex, int] = {}
        for move in wire.split(","):
            d, q = move[0], int(move[1:])
            for _ in range(q):
                pos += dir[d]
                c += 1
                if pos not in visited:
                    visited[pos] = c
        return visited

    wires = list(map(get_steps, data.splitlines()))
    inte: set[complex] | None = None
    for wire in wires:
        if inte is None:
            inte = set(wire.keys())
        else:
            inte.intersection_update(set(wire.keys()))
    assert inte is not None
    return min(sum(wire[point] for wire in wires) for point in inte)


print(part1(input))
print(part2(input))
