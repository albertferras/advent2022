import re
import sys
from utils import printchr, bcolors

DIRECTIONS = [
    complex(1, 0),  # right
    complex(0, 1),  # down
    complex(-1, 0),  # left
    complex(0, -1),  # up
]


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
    # process data input here

    tmap = {}
    start = None
    moves = []
    ymin = {}
    ymax = {}
    for y, line in enumerate(data, start=1):
        if not line:
            continue
        if line[0] in (" ", ".", "#"):
            line = line.rstrip()
            xmin = None
            xmax = None
            for x, value in enumerate(line, start=1):
                if value == " ":
                    continue
                if start is None and value == ".":
                    start = complex(x, y)
                tmap[complex(x, y)] = value
                xmin = min(xmin or x, x)
                xmax = max(xmax or x, x)
                ymin[x] = min(ymin.get(x, y), y)
                ymax[x] = max(ymax.get(x, y), y)
            tmap[complex(xmax + 1, y)] = complex(xmin, y)
            tmap[complex(xmin - 1, y)] = complex(xmax, y)
        else:
            moves = re.findall(r"(\d+|[LR]+)", line.strip())

    for x, y in ymin.items():
        tmap[complex(x, y - 1)] = complex(x, ymax[x])
        tmap[complex(x, ymax[x] + 1)] = complex(x, y)
    return tmap, moves, start


def solve():
    tmap, moves, p = read()

    direction = 0
    for move in moves:
        print(move, p)
        if move.isdigit():
            steps = int(move)
            while steps > 0:
                nextp = p + DIRECTIONS[direction]
                nextval = tmap[nextp]
                if isinstance(nextval, complex):
                    nextp = tmap[nextp]
                    nextval = tmap[nextp]
                if nextval == '#':
                    break
                steps -= 1
                print(' ', nextp, nextval)
                p = nextp
        elif move == "R":
            direction = (direction + 1) % 4
            print("NEW DIR", DIRECTIONS[direction])
        elif move == "L":
            direction = (direction - 1) % 4
            print("NEW DIR", DIRECTIONS[direction])
        else:
            raise ValueError("UNKNOWN MOVE", move)

    print("RESULT = ", 1000 * int(p.imag) + 4 * int(p.real) + direction)


solve()
