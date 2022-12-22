import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Optional


def read():
    if "sample" in sys.argv:
        data = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".split("\n")
    else:
        with open('d21_input.txt') as f:
            data = f.read().split("\n")
    return [x.split(": ") for x in data if x]


@dataclass
class Monkey:
    name: str = None
    parents: List["Monkey"] = None
    op: str = None
    number: Optional[int] = None
    depends_on: List["Monkey"] = None

    def __str__(self):
        if self.depends_on:
            s = f"{self.depends_on[0].name}{self.op}{self.depends_on[1].name} = {self.number}"
        else:
            s = str(self.number)
        return f"{self.name} [{self.number}] = {s}"

    __repr__ = __str__


def read_monkeys():
    monkeys = defaultdict(lambda: Monkey())
    for monkey_id, job in read():
        monkey = monkeys[monkey_id]
        monkey.name = monkey_id
        if job.isdigit():
            monkey.number = int(job)
        else:
            m1, op, m2 = job.split(" ")
            monkey.depends_on = [monkeys[m1], monkeys[m2]]
            monkey.op = op

    for mid, m in monkeys.items():
        for cm in (m.depends_on or []):
            if cm.parents is None:
                cm.parents = []
            cm.parents.append(m)

    return monkeys


def run(monkeys):
    q = [monkeys['root']]
    while q:
        m = q[-1]
        if m.number:
            q.pop()
            continue

        m1_child, m2_child = m.depends_on
        if m1_child.number is not None and m2_child.number is not None:
            if m.op == '+':
                m.number = m1_child.number + m2_child.number
            elif m.op == '-':
                m.number = m1_child.number - m2_child.number
            elif m.op == '/':
                m.number = m1_child.number / m2_child.number
            elif m.op == '*':
                m.number = m1_child.number * m2_child.number
            elif m.op == '=':
                m.number = m1_child.number == m2_child.number
            else:
                raise ValueError(m.op)
            q.pop()
        else:
            if m1_child.number is None:
                q.append(m1_child)
            if m2_child.number is None:
                q.append(m2_child)
    return monkeys


def reset(monkeys):
    for m in monkeys.values():
        if m.depends_on:
            m.number = None


def solve():
    monkeys = read_monkeys()
    run(monkeys)
    print("Part 1 = ", int(monkeys['root'].number))


def solve2():
    monkeys = read_monkeys()

    me = monkeys['humn']
    root = monkeys['root']
    root.op = '='
    m1, m2 = monkeys['root'].depends_on

    me.number = 0
    run(monkeys)
    delta = 1000
    while root.number != 1:
        last_x = me.number
        last_m1 = m1.number
        me.number += delta

        reset(monkeys)
        run(monkeys)
        delta = (me.number - last_x) * (m2.number - m1.number) / (m1.number - last_m1)
    print("Part2 = ", int(me.number))


def solve2b():
    monkeys = read_monkeys()
    run(monkeys)

    monkeys['root'].op = '='
    path = []
    m = monkeys['humn']
    while m != monkeys['root']:
        path.append(m)
        m = m.parents[0]
    path.append(m)
    path = path[::-1]

    target_value = path[0].number
    for i in range(len(path) - 1):
        m = path[i]
        m1, m2 = m.depends_on
        if path[i+1].name == m1.name:
            if m.op == '=':
                target_value = m2.number
            elif m.op == '+':
                target_value -= m2.number
            elif m.op == '-':
                target_value += m2.number
            elif m.op == '/':
                target_value *= m2.number
            elif m.op == '*':
                target_value /= m2.number
        else:
            if m.op == '=':
                target_value = m1.number
            elif m.op == '+':
                target_value -= m1.number
            elif m.op == '-':
                target_value = m1.number - target_value
            elif m.op == '/':
                target_value = m1.number / target_value
            elif m.op == '*':
                target_value /= m1.number
    print("RESULT = ", target_value)

# solve()
solve2()

solve2b()
