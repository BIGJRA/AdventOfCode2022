from aocd import lines, submit


##############################

def part1():
    curr_max = 0
    curr_sum = 0
    for line in lines:
        if line == '':
            curr_max = max(curr_sum, curr_max)
            curr_sum = 0
        elif line != '':
            curr_sum += int(line)
    return curr_max
print (part1())
# submit(part1())

##############################

def part2():
    curr_maxes = [0, 0, 0]
    curr_sum = 0
    for line in lines:
        if line == '':
            curr_maxes = sorted(curr_maxes + [curr_sum], reverse=True)[:3]
            curr_sum = 0
        elif line != '':
            curr_sum += int(line)
    return sum(curr_maxes)

print (part2())
# submit(part2())
