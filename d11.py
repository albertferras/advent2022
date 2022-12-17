from copy import copy
import re
from pprint import pprint
from typing import List

DEBUG = False

with open('d11_input.txt') as f:
# with open('d11_sample.txt') as f:
    txt = f.read()
txt = re.sub("Monkey ([\d]):", "monkey_\g<1> = {", txt)
txt = re.sub("Starting items: ([\d, ]*)", "'start_items': [\g<1>],", txt)
txt = re.sub("Operation: new = old ([+|*]) ([\dold]+)", "'op': ('\g<1>', '\g<2>'),", txt)
txt = re.sub("Test: divisible by ([\d]+)", "'test_divisible': \g<1>,", txt)
txt = re.sub("If true: throw to monkey ([\d]+)", "'test_true_monkey': \g<1>,", txt)
txt = re.sub("If false: throw to monkey ([\d]+)", "'test_false_monkey': \g<1>}", txt)

vars = re.findall("monkey_([\d])", txt)
txt += f"""
monkeys = {{{"".join(str(x)+": monkey_"+str(x)+"," for x in vars)}}}
"""
with open("d11_input.py", "w") as f:
    f.write(txt)

from d11_input import *
monkey_ids = list(range(len(monkeys)))


def do_round(state):
    for m in monkey_ids:
        monkey = monkeys[m]
        state[m]["inspected"] += len(state[m]["items"])
        for worry_level in state[m]['items']:
            op, val = monkey["op"]
            if val == "old":
                val = worry_level

            new_worry_level = worry_level
            if op == "+":
                new_worry_level += int(val)
            elif op == "*":
                new_worry_level *= int(val)
            new_worry_level = int(new_worry_level / 3)
            if new_worry_level % monkey["test_divisible"] == 0:
                m2 = monkey["test_true_monkey"]
            else:
                m2 = monkey["test_false_monkey"]
            state[m2]["items"].append(new_worry_level)
        state[m]['items'] = []


def print_state(state):
    for m in monkey_ids:
        print(f"Monkey {m} = {', '.join(map(str, state[m]['items']))}")


# PART 1
def part1():
    print("PART 1 --------")
    state = {
        m: {"items": copy(monkeys[m]["start_items"]), "inspected": 0}
        for m in monkey_ids
    }
    if DEBUG:
        print("Initial state")
        print_state(state)
    for r in range(1, 20 + 1):
        do_round(state)
        if DEBUG:
            print("After round ", r, "result: ")
            print_state(state)
            input()

    for m in monkey_ids:
        print(f"Monkey {m} inspected {state[m]['inspected']} items")

    top = sorted([m['inspected'] for m in state.values()], reverse=True)[:2]
    print("Part1 result = ", top[0] * top[1])


# PART 2
def do_round_new(state):
    for m in monkey_ids:
        monkey = monkeys[m]
        state[m]["inspected"] += len(state[m]["items"])
        worry_level: HNumber
        for worry_level in state[m]['items']:
            op, val = monkey["op"]
            if val == "old":
                val = worry_level
            else:
                val = int(val)

            if op == "+":
                worry_level.add(val)
            elif op == "*":
                worry_level.mul(val)
            if worry_level.is_divisible(monkey["test_divisible"]):
                m2 = monkey["test_true_monkey"]
            else:
                m2 = monkey["test_false_monkey"]
            state[m2]["items"].append(worry_level)
        state[m]['items'] = []


class HNumber:
    def __init__(self, x, factors: List[int]):
        self.orig = x
        self.div_factor = {f: x % f for f in factors}

    def is_divisible(self, a):
        return self.div_factor[a] == 0

    def add(self, a):
        for f, r in self.div_factor.items():
            self.div_factor[f] = (r + a) % f

    def mul(self, a):
        for f, r in self.div_factor.items():
            if isinstance(a, HNumber):
                self.div_factor[f] = (r * a.div_factor[f]) % f
            else:
                self.div_factor[f] = (r * a) % f

    def __str__(self):
        return f"[{self.orig}={str(self.div_factor)}]"

    __repr__ = __str__


def part2():
    print("PART 2 --------")
    factors = [m["test_divisible"] for m in monkeys.values()]
    state = {
        m: {
            "items": [HNumber(int(x), factors) for x in monkeys[m]["start_items"]],
            "inspected": 0,
        }
        for m in monkey_ids
    }
    if DEBUG:
        pprint(state)
        print("Initial state")
        print_state(state)
    for r in range(1, 10000+1):
        do_round_new(state)
        if DEBUG:
            print("After round ", r, "result: ")
            print_state(state)
            input()

    for m in monkey_ids:
        print(f"Monkey {m} inspected {state[m]['inspected']} items")

    top = sorted([m['inspected'] for m in state.values()], reverse=True)[:2]
    print("Part2 result = ", top[0] * top[1])

import sys
DEBUG = "debug" in sys.argv
part1()
part2()
