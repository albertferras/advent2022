def printmap(knots, visited):
    ax = min(x for x, y in visited) - 5
    bx = max(x for x, y in visited) + 5
    ay = min(y for x, y in visited) - 5
    by = max(y for x, y in visited) + 5
    for y in range(ay, by)[::-1]:
        for x in range(ax, bx):
            xy = Position(x, y)
            if knots[0] == xy:
                print("H", end='')
            else:
                isk = False
                k = 0
                for k, K in enumerate(knots[1:], start=1):
                    if K == xy:
                        isk = True
                        break
                if isk:
                    print(str(k), end='')
                elif (xy.x, xy.y) in visited:
                    print("x", end='')
                elif y == 0:
                    print("-", end='')
                elif x == 0:
                    print("|", end='')
                else:
                    print(".", end='')
        print(f" # {y}")


class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def move(self, other: "Position"):
        self.x += other.x
        self.y += other.y

    def __eq__(self, other: "Position"):
        return self.x == other.x and self.y == other.y

    def touching(self, other: "Position"):
        return (
            abs(self.x - other.x) <= 1
            and abs(self.y - other.y) <= 1
        )

    def follow(self, other: "Position"):
        if not self.touching(other):
            self.x += max(-1, min(1, other.x - self.x))
            self.y += max(-1, min(1, other.y - self.y))
            return True
        return False


DIRECTIONS = {
    "L": Position(-1, 0),
    "R": Position(1, 0),
    "U": Position(0, 1),
    "D": Position(0, -1)
}


def readfile():
    with open('d9_input.txt') as f:
        for line in f:
            if not line:
                continue
            parts = line.strip().split()
            direction = DIRECTIONS[parts[0]]
            steps = int(parts[1])
            yield direction, steps


def solve(num_knots=1):
    knots = [Position() for _ in range(num_knots + 1)]
    visited = {(0, 0)}
    for i, (direction, steps) in enumerate(readfile()):
        while steps > 0:
            knots[0].move(direction)
            for k in range(len(knots)-1):
                k1 = knots[k]
                k2 = knots[k+1]
                if not k2.follow(k1):
                    break
            visited.add((knots[-1].x, knots[-1].y))
            steps -= 1
    printmap(knots, visited)
    print("Total positions:", len(visited))


solve(num_knots=1)
solve(num_knots=9)
