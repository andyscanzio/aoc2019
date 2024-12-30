from functools import cache
from util import load_inputs
from collections import deque

test, input = load_inputs("6")


def part1(data: str) -> int:
    orbits: dict[str, list[str]] = {}
    for orbit in data.splitlines():
        a, b = orbit.split(")")
        if a in orbits:
            orbits[a].append(b)
        else:
            orbits[a] = [b]

    @cache
    def dfs(node: str) -> int:
        if node not in orbits:
            return 0
        return sum(1 + dfs(new_node) for new_node in orbits[node])

    return sum(dfs(node) for node in orbits)


def part2(data: str) -> int:
    graph: dict[str, list[str]] = {}
    for orbit in data.splitlines():
        a, b = orbit.split(")")
        if a in graph:
            graph[a].append(b)
        else:
            graph[a] = [b]
        if b in graph:
            graph[b].append(a)
        else:
            graph[b] = [a]

    queue: deque[str] = deque()
    parent: dict[str, str] = {"YOU": ""}
    queue.append("YOU")
    while len(queue) != 0:
        node = queue.popleft()
        if node == "SAN":
            break
        for edge in graph[node]:
            if edge not in parent:
                parent[edge] = node
                queue.append(edge)
    node = "SAN"
    c = -1
    while parent[node] != "YOU":
        c += 1
        node = parent[node]
    return c


print(part1(input))
print(part2(input))
