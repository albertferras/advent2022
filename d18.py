import sys
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


def flood_fill(sides, cubes):
    min_xyz = (min(x for x, y, z in sides), min(y for x, y, z in sides), min(z for x, y, z in sides))
    max_xyz = (max(x for x, y, z in sides), max(y for x, y, z in sides), max(z for x, y, z in sides))

    # fifo
    q = [min_xyz]
    visited = set()
    while q:
        xyz = q.pop()
        visited.add(xyz)
        for xyz2 in neighbors(*xyz):
            if (
                min_xyz[0] <= xyz2[0] <= max_xyz[0]
                and min_xyz[1] <= xyz2[1] <= max_xyz[1]
                and min_xyz[2] <= xyz2[2] <= max_xyz[2]
                and xyz2 not in visited
                and xyz2 not in cubes
            ):
                q.append(xyz2)

    return {xyz: cnt for xyz, cnt in sides.items() if xyz in visited}


def solve():
    cubes = set()
    sides = defaultdict(int)
    for x, y, z in read():
        cubes.add((x, y, z))
        for xyz2 in neighbors(x, y, z):
            sides[xyz2] += 1

    non_cube_sides = {xyz: cnt for xyz, cnt in sides.items() if xyz not in cubes}
    print("Sides=", sum(non_cube_sides.values()))

    flooded_sides = flood_fill(non_cube_sides, cubes)
    print("Flooded Sides=", sum(flooded_sides.values()))


solve()
