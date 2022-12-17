import math
from itertools import zip_longest
from functools import cmp_to_key


INPUT_FILE = 'd13_input.txt'


def read():
    with open(INPUT_FILE) as f:
        lines = iter(f)
        while True:
            raw1 = next(lines, '')
            raw2 = next(lines, '')
            if not raw1 or not raw2:
                break
            yield eval(raw1), eval(raw2)
            next(lines, '')  # skip empty line


def right_order(p1, p2):
    for a, b in zip_longest(p1, p2):
        if a is None:
            return True
        if b is None:
            return False
        isright = None
        if isinstance(a, int) and isinstance(b, int):
            if a != b:
                return a < b
        elif isinstance(a, list) and isinstance(b, list):
            isright = right_order(a, b)
        elif isinstance(a, int):
            isright = right_order([a], b)
        elif isinstance(b, int):
            isright = right_order(a, [b])
        if isright is not None:
            return isright
    return None


def solve():
    print("PART 1 --------")
    result = 0
    for idx, (p1, p2) in enumerate(read(), start=1):
        if right_order(p1, p2):
            result += idx
    print("Result", result)


def solve2():
    print("PART 2 --------")
    p1 = [[2]]
    p2 = [[6]]
    packets = [p1, p2]
    for a, b in read():
        packets.extend([a, b])

    def cmp(a, b):
        isright = right_order(a, b)
        if isright is None:
            return 0
        return -1 if isright else 1
    packets.sort(key=cmp_to_key(cmp))
    print("Result", math.prod(packets.index(p)+1 for p in (p1, p2)))


solve()
solve2()
