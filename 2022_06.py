from aocd import lines, submit
from collections import defaultdict


def solve(part_no):
    text = lines[0]
    num_chars = {1: 4, 2: 14}[part_no]
    totals = defaultdict(lambda: 0)
    for index in range(num_chars):
        totals[text[index]] += 1
    for index in range(num_chars, len(lines[0])):
        totals[text[index]] += 1
        totals[text[index - num_chars]] -= 1
        if list(totals.values()).count(1) == num_chars:
            return index + 1
    return -1


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
