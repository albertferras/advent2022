import sys
from utils import printchr, bcolors

def read():
    if "sample" in sys.argv:
        data = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
""".split("\n")
    else:
        with open('d25_input.txt') as f:
            data = f.read().split("\n")

    return [x for x in data if x]


def snafu2n(val):
    x = 0
    for i, c in enumerate(val):
        p = 5 ** (len(val) - i - 1)
        if c == '1':
            v = 1
        elif c == '2':
            v = 2
        elif c == '-':
            v = -1
        elif c == '=':
            v = -2
        elif c == '0':
            v = 0
        else:
            raise ValueError(c)
        x += v * p
    return x


def n2snafu(x):
    s = ""
    while x:
        if x % 5 == 3:
            s = f"={s}"
            x = (x+2) // 5
        elif x % 5 == 4:
            s = f"-{s}"
            x = (x+1) // 5
        elif 0 <= x % 5 < 3:
            s = f"{x%5}{s}"
            x = x // 5
        else:
            raise ValueError("WUat", x)
    return s


def solve():
    sumx = 0
    for val in read():
        sumx += snafu2n(val)
    print(f"Result={sumx}")
    print(n2snafu(sumx))


solve()
