SOM_SIZE = 14

with open('d6_input.txt') as f:
    data = f.read()
    marker = None
    for i, c in enumerate(data, start=SOM_SIZE):
        if len(set(data[i-SOM_SIZE:i])) == SOM_SIZE:
            marker = i
            break
    print("Start", marker)
