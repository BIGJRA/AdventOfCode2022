from aocd import lines, submit
from collections import defaultdict
#############################
def evaluate(NUM_CHARS):
    text = lines[0]
    totals = defaultdict(lambda: 0)
    for index in range(NUM_CHARS):
        totals[text[index]] += 1
    for index in range(NUM_CHARS, len(lines[0])):
        totals[text[index]] += 1
        totals[text[index - NUM_CHARS]] -= 1
        if list(totals.values()).count(1) == NUM_CHARS:
            return index + 1
    return -1

def part1():
    return evaluate(4)
# submit(part1())
def part2():
    return evaluate(14)
# submit(part2())
