import contextlib
import math
from pprint import pprint
import dataclasses
import sys
import re
from typing import List

from utils import printchr, bcolors
from collections import defaultdict


class Valve:
    def __init__(self, id, rate, leadsto):
        self.id = id
        self.rate = rate
        self.leadsto = leadsto
        self.visited = False

    @contextlib.contextmanager
    def visit(self):
        oldv = self.visited
        self.visited = True
        yield
        self.visited = oldv

    def __str__(self):
        return f"{self.id}[{self.rate}]"

    __repr__ = __str__


def read():
    if "sample" in sys.argv:
        data = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".split(
            "\n"
        )
    else:
        with open("d16_input.txt") as f:
            data = f.read().split("\n")
    # process data input here
    valves = []
    for line in data:
        line = line.strip()
        if line:
            values = re.findall(r"Valve ([\w]+) has flow rate=([\d-]+); tunnels? leads? to valves? (.+)", line)[0]
            valve_id = values[0]
            rate = int(values[1])
            leading_to = values[2].strip().split(", ")
            valves.append(Valve(valve_id, rate, leading_to))
    return valves


def find_best(valves, shortest_paths, current: Valve, cum_pressure=0, time_left=30, best_pressure_found=0):
    with current.visit():
        best_path = [current.id]
        best_pressure = cum_pressure
        candidates = shortest_paths[current.id]
        for valve2, dist in candidates:
            if valve2.visited:
                # already open -> ignore
                continue
            new_time_left = time_left - dist - 1  # travel + open valve
            if new_time_left <= 0:
                continue
            currentv2_pressure = cum_pressure + valve2.rate * new_time_left
            path, pressure = find_best(
                valves,
                shortest_paths,
                valve2,
                currentv2_pressure,
                new_time_left,
                max(best_pressure, best_pressure_found),
            )
            if pressure and pressure > best_pressure:
                best_path = [current.id] + path
                best_pressure = pressure
    return best_path, best_pressure


def find_best_it(valves, shortest_paths, va: Valve, time_left=30):
    best_path = None
    best_pressure = 0

    va_candidates = [(v2, dist) for v2, dist in shortest_paths[va.id] if not v2.visited]
    tstart = time_left
    while time_left > 0:
        time_left -= 1

        for va2, va2_dist in va_candidates:
            if va2.visited or tstart - time_left != va2_dist:
                continue
            # option1: go there
            va2.visited = True
            path, va2_pressure = find_best_it(valves, shortest_paths, va2, time_left=time_left - 1)
            va2.visited = False
            if va2_pressure > best_pressure:
                best_path, best_pressure = path, va2_pressure

            # option2: try another (next loop)

    if best_path:
        return [va] + best_path, va.rate * tstart + best_pressure
    return [va], va.rate * tstart


superbest = 0


from tqdm import tqdm
def find_best_it_2(valves, shortest_paths, va: Valve, vb: Valve, time_left_a=30, time_left_b=30, cum_pressure=0):
    global superbest
    best_path_a = [va]
    best_path_b = [vb]
    best_pressure = cum_pressure

    va_candidates = [(v2, dist) for v2, dist in shortest_paths[va.id] if not v2.visited if dist+1 < time_left_a]
    tstart = time_left_a
    if time_left_a == time_left_b == 26:
        va_candidates = tqdm(va_candidates)
    for v2, dist in va_candidates:
        time_left_a = tstart - dist - 1
        # option1: go there
        # tab = " " * time_left_a
        # print(tab, tstart, f"{va} -> {v2} | {vb}")
        v2.visited = True
        path1, path2, pressure = find_best_it_2(valves, shortest_paths, v2, vb,
                                                time_left_a=time_left_a, time_left_b=time_left_b,
                                                cum_pressure=cum_pressure + v2.rate*time_left_a)
        v2.visited = False
        if pressure > best_pressure:
            best_path_a, best_path_b, best_pressure = [va] + path1, path2, pressure
            if pressure > superbest:
                superbest = pressure
                print("NEW SUPERBEST=", pressure)

    if va.id != vb.id or time_left_a != time_left_b:
        vb_candidates = [(v2, dist) for v2, dist in shortest_paths[vb.id] if not v2.visited if dist+1 < time_left_b]
        tstart = time_left_b
        if time_left_a == time_left_b == 26:
            vb_candidates = tqdm(vb_candidates)
        for v2, dist in vb_candidates:
            time_left_b = tstart - dist - 1
            # option1: go there
            # tab = " " * time_left_b
            # print(tab, tstart, f"{va} | {vb} -> {v2}")
            v2.visited = True
            path1, path2, pressure = find_best_it_2(valves, shortest_paths, va, v2,
                                                    time_left_a=time_left_a, time_left_b=time_left_b,
                                                    cum_pressure=cum_pressure + v2.rate*time_left_b)
            v2.visited = False
            # print(tab, f"{time_left_b} ## {va} | {vb} -> {vb2} ----> {path1} {path2} {pressure}")
            if pressure > best_pressure:
                best_path_a, best_path_b, best_pressure = path1, [vb] + path2, pressure
                if pressure > superbest:
                    superbest = pressure
                    print("NEW SUPERBEST=", pressure)
            # option2: try another (next loop)

    return (
        best_path_a,
        best_path_b,
        best_pressure,
    )


from tqdm import tqdm
best_pressure_ever = 0
def find_best_it_3(valves, shortest_paths,
                   va: Valve, time_left_a,
                   vb: Valve, time_left_b,
                   cum_pressure=0, tryboth=True):
    global best_pressure_ever
    if cum_pressure > best_pressure_ever:
        best_pressure_ever = cum_pressure
        print("NEW BESTPRESSURE=", cum_pressure)

    va_candidates = [(v2, dist) for v2, dist in shortest_paths[va.id] if not v2.visited if dist+1 < time_left_a]
    # if sum(max(0, (time_left_a - 2 + time_left_b - 2)) * v2.rate
    #        for v2, dist in va_candidates) + cum_pressure < best_pressure_ever:
    #     return
    tstart = time_left_a
    if time_left_a == time_left_b == 26:
        va_candidates = tqdm(va_candidates)
    for v2, dist in va_candidates:
        time_left_a = tstart - dist - 1
        v2.visited = True
        find_best_it_3(valves, shortest_paths,
                       v2, time_left_a,
                       vb, time_left_b,
                       cum_pressure=cum_pressure + v2.rate*time_left_a)
        v2.visited = False
    if va.id == vb.id and time_left_a == time_left_b:
        return
    if tryboth:
        find_best_it_3(valves, shortest_paths,
                       vb, time_left_b,
                       va, time_left_a,
                       cum_pressure=cum_pressure, tryboth=False)

class Node:
    def __init__(self, valve: Valve):
        self.valve = valve
        self.parent = None
        self.dist = math.inf


class FindShortestPath:
    def __init__(self, valves, start: str, end: str):
        self.nodes = {vid: Node(valves[vid]) for vid in valves}
        self.start = start.id
        self.end = end.id

    def run(self):
        self.nodes[self.start].dist = 0
        Q = [n for n in self.nodes.values()]
        while Q:
            u = min(Q, key=lambda n: n.dist)
            if u.valve.id == self.end:
                n_end = u
                break
            Q.remove(u)

            alt = u.dist + 1
            for v2 in u.valve.leadsto:
                n2 = self.nodes[v2]
                if alt < n2.dist:
                    n2.dist = alt
                    n2.parent = u

        # build path
        path = [n_end.valve.id]
        v = n_end
        while v.valve.id != self.start:
            v = v.parent
            path.append(v.valve.id)
        return path[::-1], len(path) - 1


def find_relevant_shortest_paths(valves):
    origin = valves["AA"]
    valves_with_rate = [v for v in valves.values() if v.rate > 0]
    shortest_paths = defaultdict(dict)
    for v1 in [origin] + valves_with_rate:
        for v2 in valves_with_rate:
            if v1.id == v2.id:
                continue
            path, dist = FindShortestPath(valves, v1, v2).run()
            shortest_paths[v1.id][v2.id] = dist

    return {
        n1: sorted([(valves[n2], dist) for n2, dist in shortest_paths[n1].items()], key=lambda n: n[1], reverse=True)
        for n1 in shortest_paths.keys()
    }


def solve():
    valves = {v.id: v for v in read()}

    current = valves["AA"]
    current.visited = True

    shortest_paths = find_relevant_shortest_paths(valves)
    # for v1v2, valvepath in sorted(shortest_paths.items()):
    #     print(v1v2, valvepath)

    # best_path, best_pressure = find_best_it(valves, shortest_paths, valves["AA"], time_left=30)
    best_path, best_pressure = find_best_it(valves, shortest_paths, valves["AA"])
    print(best_path, best_pressure)


def solve2():
    valves = {v.id: v for v in read()}

    current = valves["AA"]
    current.visited = True

    shortest_paths = find_relevant_shortest_paths(valves)
    for v1v2, valvepath in sorted(shortest_paths.items()):
        print(v1v2, valvepath)

    find_best_it_3(valves, shortest_paths, va=valves["AA"], time_left_a=26, vb=valves["AA"], time_left_b=26)
    print("pressure=", best_pressure_ever)


# solve()
solve2()
