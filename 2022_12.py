from aocd import lines, submit
from collections import deque


def solve(part_no):
    # Breadth first search time
    def get_starts_and_end(part_num):
        s = []
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == 'S' or (part_num == 2 and char == 'a'): # part 2 starts at any 'a'
                    s.append((i, j))
                elif char == 'E':
                    e = (i, j)
        return s, e

    def lookup_val(coord_tuple):
        x, y = coord_tuple
        char = lines[x][y]
        d = {'S': 'a', 'E': 'z'}
        if char in d:
            char = d[char]
        return ord(char)

    def get_neighbors(coord_tuple):
        x, y = coord_tuple
        if x > 0:
            yield x - 1, y
        if x < m - 1:
            yield x + 1, y
        if y > 0:
            yield x, y - 1
        if y < n - 1:
            yield x, y + 1

    m, n = len(lines), len(lines[0])
    starts, end = get_starts_and_end(part_no)
    # Part 1 we can start either way with equal worst-case time
    # Part 2 it is easier to search from the one end until we find a start
    # so we can work backwards from the end. => Queue starts with just end.
    queue = deque([(end, 0)])
    vis = {end}
    while queue:
        curr, best = queue.popleft()
        if curr in starts:  # will happen at least once, guaranteed.
            return best
        for neighbor in get_neighbors(curr):
            if neighbor not in vis and lookup_val(curr) - lookup_val(neighbor) <= 1:
                vis.add(neighbor);
                queue.append((neighbor, best + 1))
    return -1  # for testing, should never occur


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
