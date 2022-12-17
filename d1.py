elfs = []
with open("d1_input.txt") as f:
    elf = []
    for calories in f:
        calories = calories.strip()
        if calories:
            elf.append(int(calories))
        else:
            elfs.append(sum(elf))
            elf = []
print(max(elfs))
print(sum(sorted(elfs, reverse=True)[:3]))
