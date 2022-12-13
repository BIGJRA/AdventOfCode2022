from aocd import lines, submit


def solve(part_no):
    class Dir:
        def __init__(self, size=0, parent=None):
            self.size = size
            self.children = {}
            self.parent = parent

    tree = Dir()
    curr = tree
    part1_total = 0
    dir_sizes = []
    for line in lines:
        if line == '$ cd /':
            curr = tree
        elif line == '$ cd ..':  # Calculate dir sizes at this step.
            curr.size = sum([child.size for child in curr.children.values()])
            if curr.size <= 100000:
                part1_total += curr.size
            dir_sizes.append(curr.size)
            curr = curr.parent
        elif line[0:5] == '$ cd ':
            curr = curr.children[line[5:]]
        elif line == '$ ls':
            pass
        elif line[0:4] == 'dir ':
            curr.children[line[4:]] = Dir(parent=curr)
        else:
            curr.children[line.split()[1]] = Dir(parent=curr, size=int(line.split()[0]))
    # We don't finish by cd ..'ing back to the top,
    # so we need to finish out this branch and add directory sizes to the remaining branch nodes
    while curr is not None:
        curr.size = sum([child.size for child in curr.children.values()])
        if curr.size <= 100000:
            part1_total += curr.size
        dir_sizes.append(curr.size)
        curr = curr.parent
    target = 30000000 - (70000000 - tree.size)
    dir_sizes.sort()
    for dir_size in dir_sizes:
        if dir_size >= target:
            part2_size = dir_size
            break
    if part_no == 1:
        return part1_total
    return part2_size


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
