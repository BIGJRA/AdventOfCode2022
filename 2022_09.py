from operator import sub, add

from aocd import lines, submit
#############################

def part1():
    def get_new_head_and_tail(old_head, old_tail, direction):
        if direction == "R":
            new_head = (old_head[0] + 1, old_head[1])
            if old_tail[0] + 1 == old_head[0]:
                new_tail = (new_head[0] - 1, old_head[1])
            else:
                new_tail = old_tail
        elif direction == "L":
            new_head = (old_head[0] - 1, old_head[1])
            if old_tail[0] - 1 == old_head[0]:
                new_tail = (new_head[0] + 1, old_head[1])
            else:
                new_tail = old_tail
        if direction == "U":
            new_head = (old_head[0], old_head[1] + 1)
            if old_tail[1] + 1 == old_head[1]:
                new_tail = (old_head[0], new_head[1] - 1)
            else:
                new_tail = old_tail
        if direction == "D":
            new_head = (old_head[0], old_head[1] - 1)
            if old_tail[1] - 1 == old_head[1]:
                new_tail = (old_head[0], new_head[1] + 1)
            else:
                new_tail = old_tail
        return new_head, new_tail
    head = (0,0)
    tail = (0,0)
    tail_visited = {(0,0)}
    for line in lines:
        direction, moves = line.split()
        for _ in range(int(moves)):
            head, tail = get_new_head_and_tail(head, tail, direction)
            tail_visited.add(tail)
    return len(list(tail_visited))

print (part1())
assert (part1() == 6357)
# submit(part1())
#############################

def part2():
    def sign(x):
        if x > 0:
            return 1
        if x < 0:
            return -1
        return 0
    def update(idx):
        nonlocal ropes
        chng_x, chng_y = ropes[idx][0] - ropes[idx - 1][0],ropes[idx][1] - ropes[idx - 1][1]
        if chng_x == 0 or chng_y == 0:
            if abs(chng_x) >= 2:
                ropes[idx][0] -= sign(chng_x)
            if abs(chng_y) >= 2:
                ropes[idx][1] -= sign(chng_y)
        elif abs(chng_x) == 2 or abs(chng_y) == 2:
            ropes[idx][0] -= sign(chng_x)
            ropes[idx][1] -= sign(chng_y)
    ropes = [[0,0] for _ in range(10)]
    visited = {(0,0)}
    for line in lines:
        direct, num = line.split()
        for _ in range(int(num)):
            ropes[0][0] += {"U": [0, 1], "D": [0, -1], "L": [-1, 0], "R": [1, 0]}[direct][0]
            ropes[0][1] += {"U": [0, 1], "D": [0, -1], "L": [-1, 0], "R": [1, 0]}[direct][1]
            for segment in range(1, 10):
                update(segment)
            visited.add(tuple(ropes[-1]))
    return len(list(visited))

print(part2())
# submit(part2())
