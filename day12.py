from __future__ import annotations

from dataclasses import dataclass
from typing import Literal
from util import load_inputs
from re import compile
from math import lcm

test, input = load_inputs("12")


@dataclass
class Moon:
    x: int
    y: int
    z: int
    vx: int = 0
    vy: int = 0
    vz: int = 0

    def apply_gravity(self, other: Moon) -> None:
        if other is self:
            return
        if self.x < other.x:
            self.vx += 1
        elif self.x > other.x:
            self.vx -= 1
        if self.y < other.y:
            self.vy += 1
        elif self.y > other.y:
            self.vy -= 1
        if self.z < other.z:
            self.vz += 1
        elif self.z > other.z:
            self.vz -= 1

    def update_position(self) -> None:
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def energy(self) -> int:
        pot = abs(self.x) + abs(self.y) + abs(self.z)
        kin = abs(self.vx) + abs(self.vy) + abs(self.vz)
        return pot * kin

    def get_component(
        self, component: Literal["x"] | Literal["y"] | Literal["z"]
    ) -> tuple[int, int]:
        if component == "x":
            return self.x, self.vx
        elif component == "y":
            return self.y, self.vy
        else:
            return self.z, self.vz


def part1(data: str, steps: int) -> int:
    pattern = compile(r"<x=(-*\d+), y=(-*\d+), z=(-*\d+)>")
    moons = [
        Moon(*map(int, m.groups()))
        for line in data.splitlines()
        if (m := pattern.match(line)) is not None
    ]
    for _ in range(steps):
        for moon in moons:
            for other in moons:
                moon.apply_gravity(other)
        for moon in moons:
            moon.update_position()

    return sum(moon.energy() for moon in moons)


def part2(data: str) -> int:

    def count_repeat(
        moons: list[Moon], component: Literal["x"] | Literal["y"] | Literal["z"]
    ) -> int:
        seen: set[tuple[tuple[int, int], ...]] = set()
        compo = tuple(moon.get_component(component) for moon in moons)
        counter = 0
        while compo not in seen:
            seen.add(compo)
            counter += 1
            for moon in moons:
                for other in moons:
                    moon.apply_gravity(other)
            for moon in moons:
                moon.update_position()
            compo = tuple(moon.get_component(component) for moon in moons)
        return counter

    pattern = compile(r"<x=(-*\d+), y=(-*\d+), z=(-*\d+)>")
    moons = [
        Moon(*map(int, m.groups()))
        for line in data.splitlines()
        if (m := pattern.match(line)) is not None
    ]
    cx = count_repeat(moons, "x")
    cy = count_repeat(moons, "y")
    cz = count_repeat(moons, "z")
    print(cx, cy, cz)
    return lcm(cx, cy, cz)


print(part1(input, 1000))
print(part2(input))
