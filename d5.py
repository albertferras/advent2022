import re
from collections import defaultdict
with open('d5_input.txt') as f:
    stacks = defaultdict(list)
    # read cranes
    lines = iter(f)
    for line in lines:
        line = line.rstrip()
        if line[1] == '1':
            break
        c = 0
        for i, j in enumerate(range(1, len(line), 4), start=1):
            crate = line[j].strip()
            if not crate:
                continue
            stacks[i].insert(0, crate)
    next(lines)

    # process
    for line in lines:
        if not line:
            break
        n, s1, s2 = map(
            int, re.findall(r"move (\d+) from (\d+) to (\d+)", line, re.I)[0]
        )
        stacks[s2].extend(stacks[s1][-n:])
        del stacks[s1][-n:]
    print(''.join(stacks[i][-1] for i in range(1, len(stacks)+1)))
