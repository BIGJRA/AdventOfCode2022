from aocd import lines, submit
import re
from collections import deque


def solve(part_no):
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
        if part_no == 1:
            for _ in range(int(moves)):  # Here we move each piece one at a time
                stacks[int(final) - 1].append(stacks[int(initial) - 1].pop())
        elif part_no == 2:
            temp_stack = []  # We use a temporary stack to move sub-stacks
            for _ in range(int(moves)):
                temp_stack.append(stacks[int(initial) - 1].pop())
            while temp_stack:
                stacks[int(final) - 1].append(temp_stack.pop())
    return ''.join([stack[-1] for stack in stacks])


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
