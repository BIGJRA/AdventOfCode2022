from aocd import lines, submit
#############################
def part1():
    summ = 0
    for line in lines:
        common_char = list(set(line[:len(line)//2]).intersection(set(line[len(line)//2:])))[0]
        summ += (1 + ord(common_char.lower()) - ord('a') + 26 * (ord(common_char) < ord('a')))
    return summ

print (part1())
# submit(part1())
#############################

def part2():
    line_groups = []
    counter = 0
    for line in lines:
        if counter == 0:
            line_groups.append([])
        line_groups[-1].append(line)
        counter = (counter + 1) % 3
    summ = 0
    for g in line_groups:
        common_char = list(set(g[0]).intersection(set(g[1])).intersection(set(g[2])))[0]
        summ += (1 + ord(common_char.lower()) - ord('a') + 26 * (ord(common_char) < ord('a')))
    return summ

print(part2())
# submit(part2())
