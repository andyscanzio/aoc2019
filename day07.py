from intcode import Intcode
from util import load_inputs
from itertools import permutations
from collections import deque

test, input = load_inputs("7")


def part1(data: str) -> int:

    def acs(a: int, b: int, c: int, d: int, e: int) -> int:
        oa, ob, oc, od, oe = (
            deque([a, 0]),
            deque([b]),
            deque([c]),
            deque([d]),
            deque([e]),
        )
        res: list[int] = []

        def input_a() -> int:
            return oa.popleft()

        def output_a(x: int) -> None:
            ob.append(x)

        def input_b() -> int:
            return ob.popleft()

        def output_b(x: int) -> None:
            oc.append(x)

        def input_c() -> int:
            return oc.popleft()

        def output_c(x: int) -> None:
            od.append(x)

        def input_d() -> int:
            return od.popleft()

        def output_d(x: int) -> None:
            oe.append(x)

        def input_e() -> int:
            return oe.popleft()

        def output_e(x: int) -> None:
            res.append(x)

        Intcode(data, input_a, output_a).run()
        Intcode(data, input_b, output_b).run()
        Intcode(data, input_c, output_c).run()
        Intcode(data, input_d, output_d).run()
        Intcode(data, input_e, output_e).run()
        return res[0]

    return max(acs(*p) for p in permutations((0, 1, 2, 3, 4)))


def part2(data: str) -> int:

    def acs(a: int, b: int, c: int, d: int, e: int) -> int:
        oa, ob, oc, od, oe = (
            deque([a, 0]),
            deque([b]),
            deque([c]),
            deque([d]),
            deque([e]),
        )
        res: list[int] = []

        def run(i: Intcode) -> None:
            if not i.has_halted():
                i.unset_interrupt()
                i.run_with_interrupt()

        def input_a() -> int:
            return oa.popleft()

        def output_a(x: int) -> None:
            ob.append(x)

        def input_b() -> int:
            return ob.popleft()

        def output_b(x: int) -> None:
            oc.append(x)

        def input_c() -> int:
            return oc.popleft()

        def output_c(x: int) -> None:
            od.append(x)

        def input_d() -> int:
            return od.popleft()

        def output_d(x: int) -> None:
            oe.append(x)

        def input_e() -> int:
            return oe.popleft()

        def output_e(x: int) -> None:
            res.append(x)
            oa.append(x)

        ia = Intcode(data, input_a, output_a)
        ib = Intcode(data, input_b, output_b)
        ic = Intcode(data, input_c, output_c)
        id = Intcode(data, input_d, output_d)
        ie = Intcode(data, input_e, output_e)
        while not (
            ia.has_halted()
            and ib.has_halted()
            and ic.has_halted()
            and id.has_halted()
            and ie.has_halted()
        ):
            run(ia)
            run(ib)
            run(ic)
            run(id)
            run(ie)
        return res[-1]

    return max(acs(*p) for p in permutations((5, 6, 7, 8, 9)))


print(part1(input))
print(part2(input))
