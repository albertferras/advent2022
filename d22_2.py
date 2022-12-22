import re
import sys
from collections import defaultdict

from utils import printchr

DEBUG = "dbg" in sys.argv

DIRECTIONS = [
    complex(1, 0),  # right
    complex(0, 1),  # down
    complex(-1, 0),  # left
    complex(0, -1),  # up
]
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

slen = 4 if "sample" in sys.argv else 50
sidetop = lambda s: complex((s % 4) * slen + 1, (s // 4) * slen + 1)
getside = lambda x, y: ((int(x) - 1) // slen + 4 * ((int(y) - 1) // slen))
getsidep = lambda p: getside(p.real, p.imag)
dirstr = lambda d: {0: ">", 1: "v", 2: "<", 3: "^"}[d]


def read():
    if "sample" in sys.argv:
        data = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
""".split(
            "\n"
        )
    else:
        with open("d22_input.txt") as f:
            data = f.read().split("\n")

    tmap = {}
    start = None
    moves = []

    sides = {}
    for y, line in enumerate(data, start=1):
        if not line:
            continue
        if line[0] in (" ", ".", "#"):
            line = line.rstrip()
            for x, value in enumerate(line, start=1):
                if value == " ":
                    continue
                if start is None and value == ".":
                    start = complex(x, y)
                tmap[complex(x, y)] = value
                side = getside(x, y)
                sides[side] = 1
        else:
            moves = re.findall(r"(\d+|[LR]+)", line.strip())

    # Draw map of sides
    print("----" * 4)
    for y in range(1, 5):
        y *= slen
        for x in range(1, 5):
            x *= slen
            side = getside(x, y)
            if side in sides:
                printchr(f"[{side:>2}]")
            else:
                printchr("    ")
        print("")
    print("----" * 4)

    rotations = {side: {} for side in sides}

    def _get_rot(side, ad):
        if ad in rotations[side]:
            return rotations[side][ad]
        side_front = getsidep(sidetop(side) + DIRECTIONS[ad] * slen)
        if side_front in sides:
            return side_front, ad
        side_r, ad_r = _get_rot(side, (ad + 1) % 4)
        side_l, ad_l = _get_rot(side_r, (ad_r - 1) % 4)
        rotations[side][ad] = side_l, (ad_l + 1) % 4
        return rotations[side][ad]

    for side in sides:
        rotations[side] = {ad: _get_rot(side, ad) for ad in range(4)}
    return tmap, moves, start, rotations


def dbgstate(tmap, visited):
    if not DEBUG:
        return
    for y in range(slen * 4):
        for x in range(slen * 4):
            p = complex(x + 1, y + 1)
            if p in visited:
                val = dirstr(visited[p])
            else:
                val = tmap.get(p, " ")
            printchr(val)
        print("")


def dbg(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def solve():
    tmap, moves, p, rotations = read()
    direction = 0
    visited = {p: direction}
    dbgstate(tmap, visited)
    for move in moves:
        dbg(f"Position={p}, side={getside(p.real, p.imag)}", sidetop(getside(p.real, p.imag)))
        dbg("  Move=", move)
        if move.isdigit():
            steps = int(move)
            while steps > 0:
                nextp = p + DIRECTIONS[direction]
                nextval = tmap.get(nextp)
                nextdir = direction
                if nextval is None:
                    # Rotation!
                    current_side = getside(p.real, p.imag)

                    next_side, nextdir = rotations[current_side][direction]
                    # Before moving to the new side, find how many steps we need to move
                    # to our left (relative to our current direction)
                    dist_to_left_side = 0
                    relative_left = direction - 1
                    p2 = p + DIRECTIONS[relative_left]
                    while getsidep(p2) == current_side:
                        dist_to_left_side += 1
                        p2 += DIRECTIONS[relative_left]

                    # topleft position of side in tmap
                    ps = sidetop(next_side)
                    # Once we move to the new side, we have a "corner point" on this side
                    # on our left (relative to the new direction)
                    if nextdir == DOWN:
                        ps += DIRECTIONS[RIGHT] * (slen - 1)
                    elif nextdir == UP:
                        ps += DIRECTIONS[DOWN] * (slen - 1)
                    elif nextdir == LEFT:
                        ps += (DIRECTIONS[DOWN] + DIRECTIONS[RIGHT]) * (slen - 1)
                    # Move same steps from our previous check, but to the right
                    nextp = ps + DIRECTIONS[(nextdir + 1) % 4] * dist_to_left_side
                    nextval = tmap[nextp]
                if nextval == "#":
                    break
                steps -= 1
                p = nextp
                visited[p] = direction = nextdir
        elif move == "R":
            direction = (direction + 1) % 4
        elif move == "L":
            direction = (direction - 1) % 4
        else:
            raise ValueError("UNKNOWN MOVE", move)
        visited[p] = direction
        dbgstate(tmap, visited)
        if DEBUG:
            input()

    print("RESULT = ", 1000 * int(p.imag) + 4 * int(p.real) + direction)


solve()
