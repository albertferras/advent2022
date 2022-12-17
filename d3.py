priotity = {}
c = 'a'
while True:
    priotity[c] = len(priotity) + 1
    if c == 'Z':
        break
    elif c == 'z':
        c = 'A'
    else:
        c = chr(ord(c) + 1)
print(priotity)
score = 0
with open("d3_input.txt") as f:
    for line in f:
        items = line.strip()
        comp_size = int(len(items) / 2)
        c1 = items[:comp_size]
        c2 = items[comp_size:]
        shared = set(c1).intersection(c2)
        if len(shared) != 1:
            raise Exception(f"Not sharing common item: {line}")
        common_item = list(shared)[0]
        score += priotity[common_item]
print("SUM", score)


# part 2
def groups():
    with open("d3_input.txt") as f:
        lines = iter(f)
        while True:
            try:
                yield next(lines).strip(), next(lines).strip(), next(lines).strip()
            except StopIteration:
                break

score = 0
for e1, e2, e3 in groups():
    shared = set(e1).intersection(e2).intersection(e3)
    if len(shared) != 1:
        raise Exception(f"Not sharing common item: {e1} {e2} {e3}")
    score += priotity[list(shared)[0]]
print("Part2 SUM", score)
