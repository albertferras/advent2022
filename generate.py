import os
for i in range(26):
    if os.path.exists(f"d{i}.py"):
        continue

    content = r'''import sys
from utils import printchr, bcolors


def read():
    if "sample" in sys.argv:
        data = """sampleinput
""".split("\n")
    else:
        with open('d$ID_input.txt') as f:
            data = f.read()
    # process data input here
    return data


def solve():
    data = read()


def solve2():
    data = read()


solve()
solve2()
'''
    with open(f"d{i}.py", "w") as f:
        f.write(content.replace("$ID", str(i)))

    with open(f"d{i}_input.txt", "w") as f:
        pass
