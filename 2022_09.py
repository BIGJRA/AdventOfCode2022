from aocd import lines, submit


def solve(part_no):
    def sign(x):
        if x > 0:
            return 1
        if x < 0:
            return -1
        return 0

    def update(idx):
        nonlocal ropes
        chng_x, chng_y = ropes[idx][0] - ropes[idx - 1][0], ropes[idx][1] - ropes[idx - 1][1]
        if chng_x == 0 or chng_y == 0:
            if abs(chng_x) >= 2:
                ropes[idx][0] -= sign(chng_x)
            if abs(chng_y) >= 2:
                ropes[idx][1] -= sign(chng_y)
        elif abs(chng_x) == 2 or abs(chng_y) == 2:
            ropes[idx][0] -= sign(chng_x)
            ropes[idx][1] -= sign(chng_y)

    num_ropes = {1: 2, 2: 10}[part_no]
    ropes = [[0, 0] for _ in range(num_ropes)]
    visited = {(0, 0)}
    for line in lines:
        direct, num = line.split()
        for _ in range(int(num)):
            ropes[0][0] += {"U": [0, 1], "D": [0, -1], "L": [-1, 0], "R": [1, 0]}[direct][0]
            ropes[0][1] += {"U": [0, 1], "D": [0, -1], "L": [-1, 0], "R": [1, 0]}[direct][1]
            for segment in range(1, num_ropes):
                update(segment)
            visited.add(tuple(ropes[-1]))
    return len(list(visited))


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
