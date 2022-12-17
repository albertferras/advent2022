instructions = []
with open('d10_input.txt') as f:
# with open('d10_sample.txt') as f:
    cycle = 0
    for line in f:
        op, *args = line.strip().split()
        if op == "addx":
            args = [int(args[0])]
            cycles = 2
        elif op == "noop":
            cycles = 1
        else:
            raise Exception(f"UNKNOWN OP {op!r}")
        instructions.append((cycle, cycle+cycles, op, *args))
        cycle += cycles


def value_at(ts):
    return 1 + sum(args[0] for a, b, op, *args in instructions if op == "addx" and b < ts)


sum_signal_strenghts = 0
for cycle_ts in (20, 60, 100, 140, 180, 220):
    sum_signal_strenghts += cycle_ts * value_at(cycle_ts)
print("Sum of signal strenghts=", sum_signal_strenghts)

for ts in range(240+1):
    x = value_at(ts+1)  # +1 why?
    if ts % 40 == 0:
        print('')
    print("#" if abs(x - (ts % 40)) <= 1 else '.', end='')
