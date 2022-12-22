import re
import sys
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

    # rotations = {}
    # while len(sides) + len(rotations)/2 != 4*4:
    #     for x in range(slen):
    #         for y in range(slen):
    #             xy = complex(x, y)
    #             if xy not in sides:
    #                 continue
    #             for d, v in enumerate(DIRECTIONS):
    #                 xy2 = xy + v
    #                 if xy2 not in sides:
    #                     # Need to check rotation
    #                     for rot in (-1, 1):  # turn left, right
    #                         xy3 = xy + v + DIRECTIONS[(d + rot) % 4]
    #                         if xy3 in sides:
    #                             rotations[(xy, xy2)] = (xy3, (d + rot) % 4)
    #                             rotations[(xy3, xy2)] = (xy, (d + rot + 2) % 4)  # opposite
    #                         if xy3 in rotations:
    #                             dbg(f"{sideid(xy)} -> {sideid(xy2)} ?")
    #                             #  ????? I surrender
    #                             pass
    # ^^^^ I surrender. I Will just create this manually (see below)

    if "sample" not in sys.argv:
        rotations = {
            1: {LEFT: (8, RIGHT), UP: (12, RIGHT), RIGHT: (2, RIGHT), DOWN: (5, DOWN)},
            2: {LEFT: (1, LEFT), UP: (12, UP), RIGHT: (9, LEFT), DOWN: (5, LEFT)},
            5: {LEFT: (8, DOWN), UP: (1, UP), RIGHT: (2, UP), DOWN: (9, DOWN)},
            8: {LEFT: (1, RIGHT), UP: (5, RIGHT), RIGHT: (9, RIGHT), DOWN: (12, DOWN)},
            9: {LEFT: (8, LEFT), UP: (5, UP), RIGHT: (2, LEFT), DOWN: (12, LEFT)},
            12: {LEFT: (1, DOWN), UP: (8, UP), RIGHT: (9, UP), DOWN: (2, DOWN)},
        }
    else:
        rotations = {
            2: {LEFT: (5, DOWN), UP: (4, DOWN), RIGHT: (11, LEFT), DOWN: (6, DOWN)},
            4: {LEFT: (11, UP), UP: (2, DOWN), RIGHT: (5, RIGHT), DOWN: (10, UP),},
            5: {LEFT: (4, LEFT), UP: (2, RIGHT), RIGHT: (6, RIGHT), DOWN: (10, RIGHT)},
            6: {LEFT: (5, LEFT), UP: (2, UP), RIGHT: (11, DOWN), DOWN: (10, DOWN)},
            10: {LEFT: (5, DOWN), UP: (6, UP), RIGHT: (11, RIGHT), DOWN: (4, UP)},
            11: {LEFT: (10, LEFT), UP: (6, LEFT), RIGHT: (2, LEFT), DOWN: (4, RIGHT)},
        }

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
