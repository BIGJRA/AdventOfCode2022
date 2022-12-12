import re
from aocd import lines, submit
from collections import deque
#############################

def part1():
    num_stacks = (len(lines[0]) + 1) // 4
    stacks = [deque([]) for _ in range(num_stacks)]
    for line in lines[:lines.index('')]: # Processes the blocks only
        if line[1] == '1': # ignores the line with numbers
            continue
        for i in range(num_stacks):
            char = line[4 * i + 1]
            if char != ' ':
                stacks[i].appendleft(char)
    for line in lines[lines.index('') + 1:]:
        moves, initial, final = re.split(r'move | from | to ', line)[1:]
        for _ in range(int(moves)):
            stacks[int(final) - 1].append(stacks[int(initial) - 1].pop())
    return ''.join([stack[-1] for stack in stacks])
print (part1())
# submit(part1())
#############################
def part2():
    num_stacks = (len(lines[0]) + 1) // 4
    stacks = [deque([]) for _ in range(num_stacks)]
    for line in lines[:lines.index('')]:  # Processes the blocks only
        if line[1] == '1':  # ignores the line with numbers
            continue
        for i in range(num_stacks):
            char = line[4 * i + 1]
            if char != ' ':
                stacks[i].appendleft(char)
    for line in lines[lines.index('') + 1:]:
        moves, initial, final = re.split(r'move | from | to ', line)[1:]
        temp_stack = deque([])
        for _ in range(int(moves)):
            temp_stack.append(stacks[int(initial) - 1].pop())
        while temp_stack:
            stacks[int(final) - 1].append(temp_stack.pop())
    return ''.join([stack[-1] for stack in stacks])
print(part2())
submit(part2())

from aocd import lines, submit

def solve(part_no):
    return part_no

p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
