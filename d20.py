import dataclasses
import sys


def read():
    if "sample" in sys.argv:
        data = """1
2
-3
3
-2
0
4
"""
    else:
        with open('d20_input.txt') as f:
            data = f.read()
    return [int(x) for x in data.split("\n") if x]


@dataclasses.dataclass
class Number:
    x: int
    position: int


def new_pos(p, n):
    return p % (n - 1)


def solve(m=1, mix_times=1):
    values = read()
    values = [Number(x * m, i) for i, x in enumerate(values)]
    size = len(values)

    mix_order = [n for n in values]
    for round_n in range(mix_times):
        print("ROUND", round_n)
        for node in mix_order:
            i = node.position
            new_i = (node.x + i) % (size - 1)
            if i == new_i:
                continue
            for n in values[i+1:]:
                n.position -= 1
            values.pop(i)
            values.insert(new_i, node)
            node.position = new_i
            for n in values[new_i+1:]:
                n.position += 1

    values = [n.x for n in values]
    z = values.index(0)
    part1_sum = 0
    for i in [1000, 2000, 3000]:
        val = values[new_pos((i+z) % size, size)]
        part1_sum += val
    print("SUM=", part1_sum)


solve(m=1)
solve(m=811589153, mix_times=10)
