from aocd import lines, submit


def solve(part_no):
    x = 1
    cycle = 0
    total = 0
    image = []

    def add_cycle():
        nonlocal cycle, total
        cycle += 1
        if (cycle + 20) % 40 == 0:
            total += (cycle * x)
        if (cycle - 1) % 40 == 0:
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
    if part_no == 1:
        return total
    if part_no == 2:
        for line in image:
            print(''.join(line))
        return "See above output!"


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(input("What letters are shown above? \n"))
