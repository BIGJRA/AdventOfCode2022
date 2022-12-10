from aocd import lines, submit
#############################

def part1():
    total = 0
    for line in lines:
        min1, max1 = map(lambda x: int(x), line.split(',')[0].split('-'))
        min2, max2 = map(lambda x: int(x), line.split(',')[1].split('-'))
        if ((min1 <= min2) and (max1 >= max2)) or ((min1 >= min2) and (max1 <= max2)):
            total += 1
    return total
print (part1())
# submit(part1())
#############################


def part2():
    total = 0
    for line in lines:
        min1, max1 = map(lambda x: int(x), line.split(',')[0].split('-'))
        min2, max2 = map(lambda x: int(x), line.split(',')[1].split('-'))
        if ((min1 <= max2) and (max1 >= min2)) or ((min1 >= max2) and (max1 <= min2)):
            total += 1
    return total

print(part2())
submit(part2())
