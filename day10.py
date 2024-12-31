from math import pi, atan2
from math import gcd
from util import load_inputs

test, input = load_inputs("10")


def part1(data: str) -> int:

    def vectors_to_check(asteroid: complex, width: int, height: int) -> set[complex]:
        vectors: set[complex] = set()
        for y in range(height):
            for x in range(width):
                point = x + 1j * y
                if point == asteroid:
                    continue
                vector = point - asteroid
                vector /= gcd(int(vector.real), int(vector.imag))
                vectors.add(vector)
        return vectors

    def collision_along_vector(
        asteroid: complex,
        vector: complex,
        asteroids: set[complex],
        width: int,
        height: int,
    ) -> bool:
        spot = asteroid + vector
        while 0 <= spot.real < width and 0 <= spot.imag < height:
            if spot in asteroids:
                return True
            spot += vector
        return False

    def count_from_asteroid(
        asteroid: complex, asteroids: set[complex], width: int, height: int
    ) -> int:
        return sum(
            collision_along_vector(asteroid, vector, asteroids, width, heigth)
            for vector in vectors_to_check(asteroid, width, heigth)
        )

    asteroids: set[complex] = set()
    for y, row in enumerate(data.splitlines()):
        for x, item in enumerate(row):
            if item == "#":
                asteroids.add(x + 1j * y)
    heigth, width = len(data), len(data.splitlines()[0])
    values = max(
        [
            (count_from_asteroid(asteroid, asteroids, width, heigth), asteroid)
            for asteroid in asteroids
        ],
        key=lambda x: x[0],
    )
    print(values)
    return values[0]


def part2(data: str, start: complex) -> int:

    def ang(vec: complex) -> float:
        a = atan2(-vec.imag, vec.real)
        if 0 <= a <= pi / 2:
            a = abs(a - pi / 2)
        elif a < 0:
            a = abs(a) + pi / 2
        else:
            a = 5 * pi / 2 - a
        return a

    def vectors_to_check(asteroid: complex, width: int, height: int) -> list[complex]:
        vectors: set[complex] = set()
        for y in range(height):
            for x in range(width):
                point = x + 1j * y
                if point == asteroid:
                    continue
                vector = point - asteroid
                vector /= gcd(int(vector.real), int(vector.imag))
                vectors.add(vector)
        return sorted(vectors, key=lambda x: ang(x))

    def collision_along_vector(
        asteroid: complex,
        vector: complex,
        asteroids: set[complex],
        width: int,
        height: int,
    ) -> complex | None:
        spot = asteroid + vector
        while 0 <= spot.real < width and 0 <= spot.imag < height:
            if spot in asteroids:
                return spot
            spot += vector
        return None

    asteroids: set[complex] = set()
    for y, row in enumerate(data.splitlines()):
        for x, item in enumerate(row):
            if item == "#":
                asteroids.add(x + 1j * y)
    heigth, width = len(data), len(data.splitlines()[0])
    total_vaporized = 0
    while total_vaporized <= 200:
        vectors = vectors_to_check(start, width, heigth)
        for vector in vectors:
            collision = collision_along_vector(start, vector, asteroids, width, heigth)
            if collision is not None:
                total_vaporized += 1
                asteroids.remove(collision)
                if total_vaporized == 200:
                    return int(collision.imag + 100 * collision.real)

    return 0


print(part1(input))
print(part2(input, 11 + 19j))
