import sys
import re
from utils import printchr, bcolors
from dataclasses import dataclass
from tqdm import tqdm


@dataclass(frozen=True)
class XY:
    x: int
    y: int


@dataclass
class Signal:
    sensor: XY
    beacon: XY


def read():
    if "sample" in sys.argv:
        data = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
""".split("\n")
    else:
        with open('d15_input.txt', "r") as f:
            data = f.read().split("\n")
    # process data input here
    signals = []
    for line in data:
        line = line.strip()
        if line:
            values = re.findall(r"Sensor at x=([\d-]+), y=([\d-]+): closest beacon is at x=([\d-]+), y=([\d-]+)", line)[0]
            values = [int(x) for x in values]
            signals.append(
                Signal(sensor=XY(values[0], values[1]),
                       beacon=XY(values[2], values[3]))
            )
    return signals


def distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)


def merge_ranges(ranges):
    result = []
    for a, b in sorted(ranges):
        if result and result[-1][1] >= a - 1:
            result[-1][1] = max(result[-1][1], b)
        else:
            result.append([a, b])
    return result


def solve():
    signals = read()
    print(f"{len(signals)} signals read")
    target_y = 10 if "sample" in sys.argv else 2000000
    xymax = 20 if "sample" in sys.argv else 4000000

    possible_holes = []
    already_occupied = set()
    for signal in signals:
        already_occupied.add(signal.sensor)
        already_occupied.add(signal.beacon)

    for y in tqdm(range(xymax)):
        ranges = []
        for signal in signals:
            range_dist = distance(signal.sensor, signal.beacon)
            dy = abs(y - signal.sensor.y)
            x1 = signal.sensor.x - range_dist + dy
            x2 = signal.sensor.x + range_dist - dy
            if x1 > x2:
                # print("Sensor", signal.sensor, "Dist:", range_dist, "Ranges: TOO FAR")
                continue
            if signal.beacon.y == y:
                # print(x1, x2, signal.beacon)
                if x1 == signal.beacon.x:
                    newranges = [(x1 + 1, x2)]
                elif x2 == signal.beacon.x:
                    newranges = [(x1, x2 - 1)]
                else:
                    assert x1 < signal.beacon.x < x2
                    newranges = [
                        (x1, signal.beacon.x - 1),
                        (signal.beacon.x + 1, x2)
                    ]
            else:
                newranges = [(x1, x2)]
            # print("Sensor", signal.sensor, "Dist:", range_dist, "Ranges: ", newranges)
            ranges.extend(newranges)

        # Unify ranges
        ranges = merge_ranges(ranges)
        # print("Ranges:", ranges)

        # DISTRESS BEACON (PART 2)
        for i in range(1, len(ranges)):
            r1 = ranges[i - 1]
            r2 = ranges[i]
            for x in range(r1[1]+1, r2[0]):
                if XY(x, y) not in already_occupied:
                    print("Possible hole", x, y, "!!! THIS")
                    print("Part2 solution:", 4000000 * x + y)

        # Covered positions ( PART 1 )
        if y == target_y:
            covered_positions = 0
            for a, b in ranges:
                covered_positions += b - a + 1
            print("Covered positions:", covered_positions)

solve()
