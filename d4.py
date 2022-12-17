def parse(x):
    a, b = x.split("-")
    a = int(a)
    b = int(b)
    return int(a), int(b)


def fully_contained(s1, s2):
    return s1[1] <= s2[1] and s1[0] >= s2[0]


def overlaps(s1, s2):
    return not (s1[0] > s2[1] or s1[1] < s2[0])


total_contained = 0
total_overlap = 0
with open('d4_input.txt') as f:
    for line in f:
        p1, p2 = line.strip().split(",")
        sections1 = parse(p1)
        sections2 = parse(p2)
        if fully_contained(sections1, sections2) or fully_contained(sections2, sections1):
            total_contained += 1

        if overlaps(sections1, sections2):
            total_overlap += 1

print("Total contained=", total_contained)
print("Total overlap=", total_overlap)
