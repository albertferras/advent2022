from collections import defaultdict

from utils import printchr, bcolors

AIR = None
ROCK = 1
SAND = 2

def read():
    ftest = """
    498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""
    with open('d14_input.txt') as f:
        data = []
        # f = ftest.split("\n")
        for line in f:
            line = line.strip()
            if not line:
                continue
            data.append([[int(x) for x in part.split(',')] for part in line.split(" -> ")])
    return data


def generate_map(traces):
    dmap = {}
    for paths in traces:
        x, y = paths[0]
        for x2, y2 in paths[1:]:
            while x != x2:
                dmap[(x, y)] = ROCK
                x += 1 if x < x2 else -1
            while y != y2:
                dmap[(x, y)] = ROCK
                y += 1 if y < y2 else -1
            x, y = x2, y2
        dmap[(x, y)] = ROCK
    return dmap


def print_map(dmap: dict):
    k = 4
    minx = min(x for x, y in dmap.keys()) - 3
    maxx = max(x for x, y in dmap.keys()) + 3
    miny = min(y for x, y in dmap.keys()) - 3
    maxy = max(y for x, y in dmap.keys()) + 3
    minx -= minx % k

    maxsand = 50
    for (x, y), val in dmap.items():
        if val == SAND:
            maxsand = max(y, maxsand)

    for digit in range(3)[::-1]:
        printchr("      ")
        for x in range(minx, maxx, k):
            printchr(int(x / (10 ** digit)) % 10, color=bcolors.FAIL if x == 500 else None)
            printchr(" " * (k - 1))
        print("")

    for y in range(min(0, miny), min(maxsand + 3, maxy)):
        printchr(f"{y:>3} | ", color=bcolors.FAIL)
        for x in range(minx, maxx):
            val = dmap.get((x, y), AIR)
            if val == AIR:
                printchr(".", color=bcolors.FAIL if x == 500 else None)
            elif val == ROCK:
                printchr("#", bcolors.WARNING)
            elif val == SAND:
                printchr("o", bcolors.OKGREEN)
            else:
                raise Exception("UNKNOWN")
        print("")


def throw_sand(dmap, x, y, maxrocky):
    while dmap.get((x, y)) == AIR:
        if maxrocky.get(x, 999) < y:
            print("end", x)
            return True
        down = dmap.get((x, y+1))
        if down == AIR:
            y += 1
        else:
            # ROCK or SAND, try diagonall
            dl = dmap.get((x - 1, y + 1))
            dr = dmap.get((x + 1, y + 1))
            if dl == AIR:
                x -= 1
                y += 1
            elif dr == AIR:
                x += 1
                y += 1
            else:
                dmap[(x, y)] = SAND
                return False


def solve():
    traces = read()
    dmap = generate_map(traces)
    maxrocky = defaultdict(int)
    for (x, y), val in dmap.items():
        maxrocky[x] = max(maxrocky[x], y)
    print(dict(maxrocky))

    i = 0
    while True:
        if throw_sand(dmap, 500, 0, maxrocky):
            break
        i += 1
        # if i % 100 == 0:
        #     print_map(dmap)
        #     input()
    print_map(dmap)
    print("FINISH", i)

solve()
