import sys
from utils import printchr, bcolors

def read():
    if "sample" in sys.argv:
        data = """sampleinput
""".split("\n")
    else:
        with open('d20_input.txt') as f:
            data = f.read()
    # process data input here
    return data


def solve():
    data = read()


def solve2():
    data = read()


solve()
solve2()
