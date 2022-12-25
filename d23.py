import sys
from collections import defaultdict

from tqdm import tqdm

from utils import printchr, bcolors

def read():
    if "sample" in sys.argv:
        data = """....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""".split("\n")
    else:
        with open('d23_input.txt') as f:
            data = f.read().split("\n")
    emap = set()
    xmin = xmax = ymin = ymax = None
    for y, line in enumerate(data, start=1):
        if ymin is None:
            ymin = y
        for x, c in enumerate(line.strip()):
            if xmin is None:
                xmin = x
            if c == '#':
                emap.add((y, x))
        xmax = x
    ymax = y
    return emap, ymin, ymax, xmin, xmax


def neighbors(y, x):
    yield y, x + 1  #, 'E'
    yield y, x - 1  #, 'W'
    yield y - 1, x + 1  #, 'NE'
    yield y - 1, x  #, 'N'
    yield y - 1, x - 1  #, 'NW'
    yield y + 1, x + 1  #, 'SE'
    yield y + 1, x  #, 'S'
    yield y + 1, x - 1  #, 'SW'


def easts(y, x):
    yield y, x + 1
    yield y - 1, x + 1
    yield y + 1, x + 1


def wests(y, x):
    yield y, x - 1
    yield y - 1, x - 1
    yield y + 1, x - 1


def norths(y, x):
    yield y - 1, x
    yield y - 1, x + 1
    yield y - 1, x - 1


def souths(y, x):
    yield y + 1, x
    yield y + 1, x + 1
    yield y + 1, x - 1


def solve():
    emap, ymin, ymax, xmin, xmax = read()
    print(len(emap), 'elfs')

    directions = [norths, souths, wests, easts]
    ymin, ymax = -1, 10
    xmin, xmax = -3, 10
    for turn in tqdm(range(1, 9999999)):
        emap2 = set()
        choices = {}
        ccnt = defaultdict(int)

        for elf in emap:
            y, x = elf

            if all(new not in emap for new in neighbors(y, x)):
                choices[elf] = elf
            else:
                for fd in directions:
                    candidates = list(fd(y, x))
                    if all(new not in emap for new in candidates):
                        choices[elf] = candidates[0]
                        break
                if elf not in choices:
                    choices[elf] = elf
            ccnt[choices[elf]] += 1

        nomoves = 0
        for elf, new in choices.items():
            if ccnt[new] == 1:
                emap2.add(new)
            else:
                emap2.add(elf)

            if new == elf:
                nomoves += 1
        print(turn, nomoves, len(emap))

        emap = emap2
        if nomoves == len(emap):
            break

        # for y in range(ymin, ymax+1):
        #     for x in range(xmin, xmax + 1):
        #         printchr('#' if (y, x) in emap else '.')
        #     print()
        # input()

        directions.append(directions.pop(0))

    ymin, ymax = min(y for y, x in emap), max(y for y, x in emap)
    xmin, xmax = min(x for y, x in emap), max(x for y, x in emap)
    for y in range(ymin, ymax + 1):
        for x in range(xmin, xmax + 1):
            printchr('#' if (y, x) in emap else '.')
        print()

    print((xmax - xmin + 1) * (ymax - ymin + 1) - len(emap))
    print("Turns:", turn)



solve()

'''
ccnt[y2, x2] == 1
ccnt[y2, x2] == 1
ccnt[y2, x2] == 1
ccnt[y2, x2] == 1
'''
