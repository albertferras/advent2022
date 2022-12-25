import sys
from collections import defaultdict

from utils import printchr, bcolors


def read():
    if "sample" in sys.argv:
        data = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
""".split(
            "\n"
        )
    else:
        with open("d24_input.txt") as f:
            data = f.read().split("\n")

    vblizzards = defaultdict(list)
    hblizzards = defaultdict(list)
    for y, line in enumerate(data, start=-1):
        line = line.strip()
        if not line:
            continue
        for x, val in enumerate(line, start=-1):
            if val == "^":
                vblizzards[x].append((y, -1))
            elif val == "v":
                vblizzards[x].append((y, 1))
            elif val == "<":
                hblizzards[y].append((x, -1))
            elif val == ">":
                hblizzards[y].append((x, 1))
    return hblizzards, vblizzards, y - 1, x


movements = [(1, 0), (0, 1), (0, 0), (-1, 0), (0, -1)]  # down  # right  # no move  # up  # left


def findbest(start, end, vbliz, hbliz, h, w, k):
    q = [(start[0], start[1], 0)]  # starting position
    visited = set()
    while q:
        y, x, dist = state = min(q, key=lambda n: n[2])
        # print(state)
        q.remove(state)
        if state in visited:
            continue
        visited.add(state)
        dist += 1
        for mov in movements:
            y2, x2 = y + mov[0], x + mov[1]
            if (y2, x2) == end:
                return dist

            if (
                0 <= y2 < h and 0 <= x2 < w
                and all((by + d * (dist+k)) % h != y2 for by, d in vbliz[x2])
                and all((bx + d * (dist+k)) % w != x2 for bx, d in hbliz[y2])
            ) or (y2, x2) == start or (y2, x2) == end:
                q.append((y2, x2, dist))
    raise ValueError("Could not find :<")


def solve():
    hbliz, vbliz, h, w = read()
    print(h, w)

    A = (-1, 0)
    B = (h, w - 1)
    dist = findbest(A, B, vbliz, hbliz, h, w, k=0)
    print(f"Dist A->B = {dist}")
    dist2 = findbest(B, A, vbliz, hbliz, h, w, k=dist)
    print(f"Dist B->A = {dist2}")
    dist3 = findbest(A, B, vbliz, hbliz, h, w, k=dist2+dist)
    print(f"Dist A->B = {dist3}")
    print(f"Total = {dist + dist2 + dist3}")


solve()
