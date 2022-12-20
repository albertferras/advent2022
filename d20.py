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


def solve(m=1, mix_times=1):
    values = read()
    values = [Number(x * m, i) for i, x in enumerate(values)]
    n = len(values)

    mix_order = [n for n in values]
    for round_n in range(mix_times):
        for node in mix_order:
            i = values.index(node)
            if node.x != 0:
                values.pop(i)
                values.insert((node.x + i) % (n - 1), node)
    values = [n.x for n in values]
    z = values.index(0)
    print(sum(values[(i+z) % n] for i in (1000, 2000, 3000)))


solve(m=1)
solve(m=811589153, mix_times=10)
