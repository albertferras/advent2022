ROCK = 1
PAPER = 2
SCISSORS = 3
P0 = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS
}
P1 = {
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS
}

def wins(A, B):
    return (
        (A == ROCK and B == SCISSORS)
        or (A == PAPER and B == ROCK)
        or (A == SCISSORS and B == PAPER)
    )


score_p0 = 0
score_p1 = 0
with open("d2_input.txt") as f:
    for line in f:
        x0, x1 = line.strip().split(" ")
        p0 = P0[x0]

        if x1 == 'X':
            if p0 == ROCK:
                p1 = SCISSORS
            elif p0 == PAPER:
                p1 = ROCK
            else:
                p1 = PAPER
        elif x1 == 'Y':
            p1 = p0
        elif x1 == 'Z':
            if p0 == ROCK:
                p1 = PAPER
            elif p0 == PAPER:
                p1 = SCISSORS
            else:
                p1 = ROCK
        else:
            raise Exception("NOPE")

        # p1 = P1[x1]
        # p1 = x1

        if wins(p1, p0):
            score_p1 += 6
        elif wins(p0, p1):
            score_p0 += 6
        else:
            assert p0 == p1
            score_p0 += 3
            score_p1 += 3
        score_p0 += p0
        score_p1 += p1


print("P0", score_p0)
print("P1", score_p1)
