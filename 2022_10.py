from aocd import lines, submit

#############################

def part1():
    x = 1
    cycle = 0
    total = 0
    def add_cycle():
        nonlocal cycle, total
        cycle += 1
        if (cycle + 20) % 40 == 0:
            total += (cycle * x)
    for line in lines:
        if line == 'noop':
            add_cycle()
        else:
            for _ in range(2):
                add_cycle()
            x += int(line.split()[1])
    return total

print (part1())
# submit(part1())
#############################

def part2():
    x = 1
    cycle = 0
    image = []
    def add_cycle():
        nonlocal cycle
        cycle += 1
        if ((cycle - 1) % 40 == 0):
            image.append([])
        if abs(((cycle - 1) % 40) - x) <= 1:
            image[(cycle - 1) // 40].append('#')
        else:
            image[(cycle - 1) // 40].append('.')

    for line in lines:
        if line == 'noop':
            add_cycle()
        else:
            for _ in range(2):
                add_cycle()
            x += int(line.split()[1])
    for line in image:
        print(''.join(line))
        # This one requires visually looking!

part2()
# submit('ELPLZGZL')