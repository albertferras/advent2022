import traceback
from pprint import pprint
from dataclasses import dataclass
from typing import Union, Dict, Optional

HD_AVAILABLE = 70000000
UPDATE_REQUIRED_SPACE = 30000000


@dataclass
class File:
    size: int


@dataclass
class Dir:
    files: Dict[str, Union["Dir", File]]
    parent: Optional["Dir"] = None
    size: int = None
    name: str = ""

    def todict(self):
        result = {k: (v.todict() if isinstance(v, Dir) else v.size) for k, v in self.files.items()}
        result['### [SIZE] ### '] = self.size
        return result

    def calc_size(self):
        totsize = 0
        for dirfile in self.files.values():
            if isinstance(dirfile, Dir):
                dirfile.calc_size()
            totsize += dirfile.size
        self.size = totsize

    def iterdirs(self):
        for dirfile in self.files.values():
            if isinstance(dirfile, Dir):
                yield dirfile
                yield from dirfile.iterdirs()

    @property
    def fullpath(self):
        path = []
        pwd = self
        while pwd:
            path.append(pwd.name)
            pwd = pwd.parent
        return "/".join(reversed(path))


def sum_dirs_size(node: Dir, max_size: int):
    # part 1
    totsize = 0
    if node.size <= max_size:
        totsize += node.size
    for dirfile in node.files.values():
        if isinstance(dirfile, Dir):
            totsize += sum_dirs_size(dirfile, max_size)
    return totsize



root = Dir({}, parent=None, name="")
pwd = root

try:
    with open('d7_input.txt') as f:
        cmd = None
        for line in f:
            line = line.strip()
            if line.startswith("$"):
                # Command
                cmd, *args = line.strip("$ ").split(" ")
                if cmd == "cd":
                    print(cmd, args)
                    if args[0] == "/":
                        pwd = root
                    elif args[0] == "..":
                        pwd = pwd.parent
                    else:
                        # fs.setdefault(args[0], {})  # autocreate on cd?
                        pwd = pwd.files[args[0]]
                elif cmd == "ls":
                    pass
            elif cmd == "ls":
                tag, name = line.strip().split()
                if tag == "dir":
                    pwd.files[name] = Dir(files={}, parent=pwd, name=name)
                else:
                    pwd.files[name] = File(size=int(tag))
except Exception:
    traceback.print_exc()
finally:
    root.calc_size()
    pprint(root.todict())

# part 1
print("Total sum dir size =", sum_dirs_size(root, 100000))

# part 2
used_space = root.size
space_to_free = used_space - (HD_AVAILABLE - UPDATE_REQUIRED_SPACE)
print("Space to free=", space_to_free)
for dir in root.iterdirs():
    print(f"{dir.fullpath} = {dir.size}")
print(min((d.size for d in root.iterdirs() if d.size >= space_to_free)))
