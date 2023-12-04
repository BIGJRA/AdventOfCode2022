from aocd import lines, submit


def solve(part_no):
    def drop_sand():
        nonlocal sand_count
        pos = (500, 0)
        if pos in occupied: # Exit condition for part 2 is when (500, 0) is covered
            return False
        while True:
            x, y = pos
            if part_no == 1 and (x < x_bounds[0] or x > x_bounds[1] or y > y_bounds[1]):
                # Exit condition for part 1: when sand exits the bounds. This happens
                # When it goes below the lowest rock, or outside the leftmost/rightmost rock.
                return False
            moved = False
            for potential in ((x, y + 1), (x - 1, y + 1), (x + 1, y + 1)):
                if potential not in occupied:
                    pos = potential
                    moved = True
                    break
            if not moved:
                occupied.add(pos)
                sand_count += 1
                return True

    occupied = set([])
    for line in lines:
        coords = line.split(' -> ')
        for i in range(1, len(coords)):
            x1, y1 = [int(x) for x in coords[i - 1].split(',')]
            x2, y2 = [int(x) for x in coords[i].split(',')]
            if x1 - x2 != 0 and y1 == y2:
                for xk in range(min(x1, x2), max(x1, x2) + 1):
                    occupied.add((xk, y1))
            elif y1 - y2 != 0 and x1 == x2:
                for yk in range(min(y1, y2), max(y1, y2) + 1):
                    occupied.add((x1, yk))
    x_bounds = [min(occupied, key=lambda x: x[0])[0], max(occupied, key=lambda x: x[0])[0]]
    y_bounds = [0, max(occupied, key=lambda x: x[1])[1]]
    if part_no == 2: # The calculated bounds help us add the floor. Note that we will never
        # go further left or right than diagonal lines down from (500, 0), hence below logic.
        for step in range(y_bounds[1] + 4):
            occupied.add((500 - step, y_bounds[1] + 2))
            occupied.add((500 + step, y_bounds[1] + 2))
    sand_count = 0
    can_drop_sand = True
    while can_drop_sand:
        can_drop_sand = drop_sand()
    return sand_count






p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
