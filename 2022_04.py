from aocd import lines, submit


def solve(part_no):
    total = 0
    for line in lines:
        min1, max1 = map(lambda x: int(x), line.split(',')[0].split('-'))
        min2, max2 = map(lambda x: int(x), line.split(',')[1].split('-'))
        if (part_no == 1 and ((min1 <= min2) and (max1 >= max2)) or ((min1 >= min2) and (max1 <= max2))) or \
                (part_no == 2 and ((min1 <= max2) and (max1 >= min2)) or ((min1 >= max2) and (max1 <= min2))):
            total += 1
    return total


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
