import math
from utils import printchr, bcolors


class Point:
    def __init__(self, level):
        self.h = ord(level) - ord('a')
        self.parent = None  # (x, y, p)
        self.dist = math.inf

    @property
    def level(self):
        return chr(self.h + ord('a'))


with open('d12_input.txt') as f:
# with open('d12_sample.txt') as f:
    S = E = (None, None)
    mmap = []
    for y, line in enumerate(f):
        row = []
        for x, tag in enumerate(line.strip()):
            if tag == 'E':
                E = (x, y)
                tag = 'z'
            elif tag == 'S':
                S = (x, y)
                tag = 'a'
            row.append(tag)
        mmap.append(row)


def printpath(mymap, path):
    print(f"----PATH----")
    print('-' * (2 + len(mymap[0])))
    for y, xxx in enumerate(mymap):
        print('|', end='')
        for x, point in enumerate(xxx):
            color = None
            if (x, y) == path[0]:
                value = 'S'
                color = bcolors.FAIL
            elif (x, y) == path[-1]:
                value = 'E'
                color = bcolors.FAIL
            elif (x, y) in path:
                value = mymap[y][x].upper()
                color = bcolors.OKGREEN
            else:
                value = mymap[y][x]
                color = None
            printchr(value, color=color)
        print('|')
    print('-' * (2 + len(mymap[0])))


def neighbors(mymap, x, y):
    if x > 0:
        yield x - 1, y
    if x < len(mymap[0]) - 1:
        yield x + 1, y
    if y > 0:
        yield x, y - 1
    if y < len(mymap) - 1:
        yield x, y + 1


class FindShortestPath:
    def __init__(self, mymap, start, end):
        self.pmap = [
            [Point(tag) for tag in xxx]
            for xxx in mymap
        ]
        self.start = start
        self.end = end

    def run(self):
        startx, starty = self.start
        self.pmap[starty][startx].dist = 0
        Q = []
        for y, xxx in enumerate(self.pmap):
            for x, point in enumerate(xxx):
                Q.append((x, y, point))

        while Q:
            u = min(Q, key=lambda xyp: xyp[2].dist)
            x, y, p = u
            if self.is_destination(x, y, p):
                end = x, y
                break
            Q.remove(u)
            for x2, y2 in neighbors(self.pmap, x, y):
                p2 = self.pmap[y2][x2]
                alt = p.dist + self.step_cost(p, p2)
                if alt < p2.dist:
                    p2.dist = alt
                    p2.parent = u

        # build path
        endx, endy = end
        x, y, p = endx, endy, self.pmap[endy][endx]
        path = [(x, y)]
        while (x, y) != self.start:
            x, y, p = self.pmap[y][x].parent
            path.append((x, y))
        return path[::-1]

    def is_destination(self, x, y, p):
        return (x, y) == self.end

    def step_cost(self, p1, p2):
        return 1 if p2.h - p1.h <= 1 else math.inf


class FindShortestPathToA(FindShortestPath):
    def is_destination(self, x, y, p):
        return p.h == 0

    def step_cost(self, p1, p2):
        return 1 if p1.h - p2.h <= 1 else math.inf


print("PART 1")
bestpath = FindShortestPath(mmap, S, E).run()
printpath(mmap, bestpath)
print("Steps=", len(bestpath) - 1)
print("\n")

print("PART 2")
bestpath = FindShortestPathToA(mmap, E, None).run()
printpath(mmap, bestpath)
print("Steps=", len(bestpath) - 1)
