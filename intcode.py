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
        self.output_buffer: list[int] = []
        self.relv_base = 0

    def parse_value(self, mode: str, pos: int, is_input: bool = False) -> int:
        match mode:
            case "0":  # Position mode
                if is_input:
                    return pos
                return self.read_data(pos)
            case "1":  # Immediate mode
                return pos
            case "2":  # Relative mode
                if is_input:
                    return pos + self.relv_base
                return self.read_data(pos + self.relv_base)
            case _:
                raise ValueError("Uknown mode")

    def parse_values(self, mode: str, *pos: int) -> tuple[int, ...]:
        if len(mode) != len(pos):
            raise ValueError("Incompatible mode")
        return tuple(self.parse_value(m, p) for m, p in zip(mode[::-1], pos))

    def write_data(self, pos: int, val: int) -> None:
        if pos >= len(self.data):
            self.data.extend([0] * (pos - len(self.data) + 1))
        self.data[pos] = val

    def read_data(self, pos: int) -> int:
        if pos >= len(self.data):
            self.data.extend([0] * (pos - len(self.data) + 1))
        return self.data[pos]

    def instruction_3(self, mode: int, op: Callable[[int, int], int]) -> None:
        p1, p2, p3 = (
            self.read_data(self.pc + 1),
            self.read_data(self.pc + 2),
            self.read_data(self.pc + 3),
        )
        v1, v2 = self.parse_values(f"{mode:03}"[1:3], p1, p2)
        v3 = self.parse_value(f"{mode:03}"[0], p3, is_input=True)
        self.write_data(v3, int(op(v1, v2)))
        self.pc += 4

    def instruction_io(self, mode: int, is_input: bool) -> None:
        p1 = self.read_data(self.pc + 1)
        v1 = self.parse_value(f"{mode:01}", p1, is_input=is_input)
        if is_input:
            if self.input is None:
                raise ValueError("Missing input function")
            self.write_data(v1, self.input())
        else:
            if self.output is None:
                self.output_buffer.append(v1)
            else:
                self.output(v1)
            self.interrupt = True
        self.pc += 2

    def instruction_jump(self, mode: int, jump_condition: bool) -> None:
        p1, p2 = self.read_data(self.pc + 1), self.read_data(self.pc + 2)
        v1, v2 = self.parse_values(f"{mode:02}", p1, p2)
        if (jump_condition and v1 != 0) or (not jump_condition and v1 == 0):
            self.pc = v2
        else:
            self.pc += 3

    def instruction_relv_base(self, mode: int) -> None:
        p1 = self.read_data(self.pc + 1)
        (v1,) = self.parse_values(f"{mode:01}", p1)
        self.relv_base += v1
        self.pc += 2

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
            case 9:
                self.instruction_relv_base(mode)
            case _:
                raise ValueError("Unknown opcode")

    def set_value(self, address: int, value: int) -> Self:
        self.write_data(address, value)
        return self

    def unset_interrupt(self) -> None:
        self.interrupt = False

    def has_halted(self) -> bool:
        return self.halted

    def run(self) -> list[int]:
        while self.pc < len(self.data) and not self.halted:
            self.opcode(self.read_data(self.pc))
        if len(self.output_buffer) > 0:
            return self.output_buffer
        return self.data

    def run_with_interrupt(self) -> list[int]:
        while self.pc < len(self.data) and not self.halted and not self.interrupt:
            self.opcode(self.read_data(self.pc))
        if len(self.output_buffer) > 0:
            return self.output_buffer
        return self.data
