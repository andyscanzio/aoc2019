from collections import Counter


def part1() -> int:
    def valid_password(password: str) -> bool:
        if not any(i >= 2 for i in Counter(password).values()):
            return False
        for i, d in enumerate(password):
            if i > 0:
                if int(d) < int(password[i - 1]):
                    return False
        return True

    return sum(valid_password(str(i)) for i in range(284639, 748759 + 1))


def part2() -> int:
    def valid_password(password: str) -> bool:
        if not any(i == 2 for i in Counter(password).values()):
            return False
        for i, d in enumerate(password):
            if i > 0:
                if int(d) < int(password[i - 1]):
                    return False
        return True

    return sum(valid_password(str(i)) for i in range(284639, 748759 + 1))


print(part1())
print(part2())
