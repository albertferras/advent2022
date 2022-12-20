import math

import numpy
from numpy.typing import ArrayLike
import dataclasses
import re
import sys
from utils import printchr, bcolors

V = lambda *a: numpy.array(a)

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3
MATERIALS = [0, 1, 2, 3]
NAME = {ORE: "ORE", CLAY: "CLAY", OBSIDIAN: "OBSI", GEODE: "GEODE", None: ""}
BUYS = [
    V(1, 0, 0, 0),
    V(0, 1, 0, 0),
    V(0, 0, 1, 0),
    V(0, 0, 0, 1)
]


@dataclasses.dataclass
class Blueprint:
    id: int
    raw: str
    recipes: dict


def read():
    if "sample" in sys.argv:
        data = """Blueprint 1:
  Each ore robot costs 4 ore.
  Each clay robot costs 2 ore.
  Each obsidian robot costs 3 ore and 14 clay.
  Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2:
  Each ore robot costs 2 ore.
  Each clay robot costs 3 ore.
  Each obsidian robot costs 3 ore and 8 clay.
  Each geode robot costs 3 ore and 12 obsidian.
"""
    else:
        with open("d19_input.txt") as f:
            data = f.read()
    # process data input here

    blueprints = []
    for block in data.split("Blueprint"):
        block = block.strip()
        if not block:
            continue
        bp_id = int(block.split(":", 1)[0])
        ore_cost = re.findall(r"Each ore robot costs (\d+) ore", block)[0]
        clay_cost = re.findall(r"Each clay robot costs (\d+) ore", block)[0]
        obsi_cost = re.findall(r"Each obsidian robot costs (\d+) ore and (\d+) clay", block)[0]
        geode_cost = re.findall(r"Each geode robot costs (\d+) ore and (\d+) obsidian", block)[0]
        blueprints.append(
            Blueprint(
                id=bp_id,
                raw=block,
                recipes={
                    ORE: V(int(ore_cost), 0, 0, 0),
                    CLAY: V(int(clay_cost), 0, 0, 0),
                    OBSIDIAN: V(int(obsi_cost[0]), int(obsi_cost[1]), 0, 0),
                    GEODE: V(int(geode_cost[0]), 0, int(geode_cost[1]), 0),
                },
            )
        )
    return blueprints


ZEROES = V(0, 0, 0, 0)


def checkbp(bp: Blueprint, last_minute):
    print("-------------")
    print(bp.raw)
    max_needed = {}
    for r in MATERIALS:
        max_needed[r] = max(v[r] for v in bp.recipes.values())
    # print("MAX NEEDED", max_needed)
    all_best = [0]

    triangle_numbers = [((n - 1) * n) // 2 for n in range(last_minute + 1)]
    print(triangle_numbers)

    def find_best(robots: ArrayLike, pocket: ArrayLike, t=1, bought=None):
        dbg = t == 1
        if dbg:
            tab = " " * t + f"T{t}:{NAME[bought]}"
            print(tab, f"Pocket={pocket}, Robots={robots}")
        # choose next robot to buy
        best_geodes = pocket[GEODE] + robots[GEODE] * (last_minute - t + 1)
        if best_geodes > all_best[0]:
            all_best[0] = best_geodes
        if best_geodes + triangle_numbers[last_minute - t + 1] < all_best[0]:
            return best_geodes

        for m in MATERIALS:
            if m != GEODE:
                if robots[m] >= max_needed[m]:
                    continue
                if pocket[m] >= max_needed[m] * 2:
                    continue
            cost = bp.recipes[m]

            pocket2 = V(*pocket)  # available at beginning of t2
            t2 = t
            while t2 < last_minute and any(cost > pocket2):
                t2 += 1
                pocket2 += robots

            if dbg:
                print(tab, f"T{t}:{NAME[m]} in T{t2}")
            if t2 < last_minute:
                robots2 = robots + BUYS[m]
                geodes2 = find_best(robots2, pocket2 + robots - cost, t2 + 1, bought=m)
                if dbg:
                    print(tab, f"T{t}:{NAME[m]} in T{t2} -> {geodes2}")
                if geodes2 > best_geodes:
                    best_geodes = geodes2
                    if best_geodes > all_best[0]:
                        all_best[0] = best_geodes
        if best_geodes > all_best[0]:
            all_best[0] = best_geodes
        return best_geodes

    print("Find best way")
    geodes = find_best(pocket=V(0, 0, 0, 0), robots=V(1, 0, 0, 0))
    print(f"Blueprint {bp.id} best geodes = {geodes}")
    return geodes


def solve(max_time, limit_bp):
    blueprints = read()[:limit_bp]
    for bp in blueprints:
        print(bp.recipes)
    part1 = 0
    results = {}
    for bp in blueprints:
        geodes = checkbp(bp, max_time)
        part1 += bp.id * geodes
        results[bp.id] = geodes
    print("Result part1=", part1)
    print("Full:", results)
    x = 1
    for geodes in results.values():
        x *= geodes
    print("Multiplication:", x)


# solve(24, 30)
solve(32, 3)
