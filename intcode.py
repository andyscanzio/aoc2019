from operator import add, mul, lt, eq
from typing import Callable, Self


class Intcode:
    def __init__(
        self,
        data: str | list[int],
        input: Callable[[], int] | None = None,
        output: Callable[[int], None] | None = None,
    ) -> None:
        if isinstance(data, str):
            self.data = list(map(int, data.split(",")))
        else:
            self.data = data
        self.pc = 0
        self.halted = False
        self.interrupt = False
        self.input = input
        self.output = output

    def parse_values(self, mode: str, *pos: int) -> tuple[int, ...]:
        if len(mode) != len(pos):
            raise ValueError("Incompatible mode")
        return tuple(p if m == "1" else self.data[p] for m, p in zip(mode[::-1], pos))

    def instruction_3(self, mode: int, op: Callable[[int, int], int]) -> None:
        p1, p2, p3 = self.data[self.pc + 1 : self.pc + 4]
        v1, v2 = self.parse_values(f"{mode:02}", p1, p2)
        self.data[p3] = op(v1, v2)
        self.pc += 4

    def instruction_io(self, mode: int, is_input: bool) -> None:
        p1 = self.data[self.pc + 1]
        v1 = self.parse_values(f"{mode:01}", p1)
        if is_input:
            if self.input is None:
                raise ValueError("Missing input function")
            self.data[p1] = self.input()
        else:
            if self.output is None:
                raise ValueError("Missing output function")
            self.output(v1[0])
            self.interrupt = True
        self.pc += 2

    def instruction_jump(self, mode: int, jump_condition: bool) -> None:
        p1, p2 = self.data[self.pc + 1 : self.pc + 3]
        v1, v2 = self.parse_values(f"{mode:02}", p1, p2)
        if (jump_condition and v1 != 0) or (not jump_condition and v1 == 0):
            self.pc = v2
        else:
            self.pc += 3

    def opcode(self, opcode: int) -> None:
        mode, code = divmod(opcode, 100)
        match code:
            case 99:
                self.halted = True
            case 1:
                self.instruction_3(mode, add)
            case 2:
                self.instruction_3(mode, mul)
            case 3:
                self.instruction_io(mode, True)
            case 4:
                self.instruction_io(mode, False)
            case 5:
                self.instruction_jump(mode, True)
            case 6:
                self.instruction_jump(mode, False)
            case 7:
                self.instruction_3(mode, lt)
            case 8:
                self.instruction_3(mode, eq)
            case _:
                raise ValueError("Unknown opcode")

    def set_value(self, address: int, value: int) -> Self:
        self.data[address] = value
        return self

    def unset_interrupt(self) -> None:
        self.interrupt = False

    def has_halted(self) -> bool:
        return self.halted

    def run(self) -> int:
        while self.pc < len(self.data) and not self.halted:
            self.opcode(self.data[self.pc])
        return self.data[0]

    def run_with_interrupt(self) -> int:
        while self.pc < len(self.data) and not self.halted and not self.interrupt:
            self.opcode(self.data[self.pc])
        return self.data[0]
