import sys
import time
from collections import defaultdict


def read():
    if "sample" in sys.argv:
        data = """2,2,2
        1,2,2
        3,2,2
        2,1,2
        2,3,2
        2,2,1
        2,2,3
        2,2,4
        2,2,6
        1,2,5
        3,2,5
        2,1,5
        2,3,5
        """
    else:
        with open("d18_input.txt") as f:
            data = f.read()
    # process data input here
    for line in data.split("\n"):
        if line.strip():
            yield [int(x) for x in line.strip().split(",")]


def neighbors(x, y, z):
    return (x - 1, y, z), (x + 1, y, z), (x, y - 1, z), (x, y + 1, z), (x, y, z - 1), (x, y, z + 1)


def flooded_sides(cubes, sides):
    minx, miny, minz = tuple(min(xyz[i] for xyz in cubes) - 1 for i in range(3))
    maxx, maxy, maxz = tuple(max(xyz[i] for xyz in cubes) + 1 for i in range(3))

    q = {(minx, miny, minz)}
    visited = set()
    while q:
        xyz = q.pop()
        visited.add(xyz)
        q.update(
            xyz2
            for xyz2 in neighbors(*xyz)
            if (
                minx <= xyz2[0] <= maxx
                and miny <= xyz2[1] <= maxy
                and minz <= xyz2[2] <= maxz
                and xyz2 not in visited
                and xyz2 not in cubes
            )
        )

    return {xyz: cnt for xyz, cnt in sides.items() if xyz in visited}


def solve():
    tstart = time.time()
    cubes = set()
    sides = defaultdict(int)
    for x, y, z in read():
        cubes.add((x, y, z))
        for xyz2 in neighbors(x, y, z):
            sides[xyz2] += 1

    non_cube_sides = {xyz: cnt for xyz, cnt in sides.items() if xyz not in cubes}
    print("Sides=", sum(non_cube_sides.values()))

    non_cube_flooded_sides = flooded_sides(cubes, non_cube_sides)
    print("Flooded Sides=", sum(non_cube_flooded_sides.values()))
    print(f"Time={time.time() - tstart:.3f}s")


solve()
