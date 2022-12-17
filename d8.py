with open('d8_input.txt') as f:
    trees = [[int(x) for x in line.strip()] for line in f.read().split("\n") if line.strip()]

visible = set()
h = len(trees)
w = len(trees[0])

for y in range(h):
    # >>>
    maxv = -1
    for x in range(w):
        v = trees[y][x]
        if v > maxv:
            visible.add((x, y))
            maxv = v
    # <<<
    maxv = -1
    for xl in range(w)[::-1]:
        x = w - xl - 1
        v = trees[y][x]
        if v > maxv:
            visible.add((x, y))
            maxv = v
for x in range(1, w-1):
    # down
    maxv = -1
    for y in range(h):
        v = trees[y][x]
        if v > maxv:
            visible.add((x, y))
            maxv = v

    # up
    maxv = -1
    for y in range(h)[::-1]:
        v = trees[y][x]
        if v > maxv:
            visible.add((x, y))
            maxv = v

# print visible trees
for y, xxx in enumerate(trees):
    for x, val in enumerate(xxx):
        print(val if (x, y) in visible else '-', end='')
    print('')
print("Num trees", len(visible))


# part 2
def score_path(x, y, dx, dy):
    score = 0
    current = trees[y][x]
    x += dx
    y += dy
    while 0 <= x <= w - 1 and 0 <= y <= h - 1:
        score += 1
        if trees[y][x] >= current:
            break
        x += dx
        y += dy
    return score


def scenic_score(x, y):
    return (
        score_path(x, y, 1, 0)
        * score_path(x, y, -1, 0)
        * score_path(x, y, 0, -1)
        * score_path(x, y, 0, 1)
    )


def best_scenic_score():
    best_score = None
    best_xy = None
    for y, vals in enumerate(trees):
        for x in range(len(vals)):
            score = scenic_score(x, y)
            if not best_score or best_score < score:
                best_score = score
                best_xy = x, y
    print("best:", best_xy, best_score)


best_scenic_score()
