from operator import add, mul
from typing import Callable, Self


class Intcode:
    def __init__(self, data: str | list[int]) -> None:
        if isinstance(data, str):
            self.data = list(map(int, data.split(",")))
        else:
            self.data = data
        self.pc = 0
        self.has_halted = False

    def instruction_3(self, op: Callable[[int, int], int]) -> None:
        p1, p2, p3 = self.data[self.pc + 1 : self.pc + 4]
        self.data[p3] = op(self.data[p1], self.data[p2])
        self.pc += 4

    def opcode(self, opcode: int) -> None:
        match opcode:
            case 99:
                self.has_halted = True
            case 1:
                self.instruction_3(add)
            case 2:
                self.instruction_3(mul)
            case _:
                raise ValueError

    def set_value(self, address: int, value: int) -> Self:
        self.data[address] = value
        return self

    def run(self, return_value: bool = False) -> int:
        while self.pc < len(self.data) and not self.has_halted:
            self.opcode(self.data[self.pc])
        return self.data[0]
