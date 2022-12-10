from aocd import lines, submit
#############################
def part1():
    def score(match):
        p1, p2 = match[0], match[1]
        if ((p1 == 'A' and p2 == 'Z') or (p1 == 'B' and p2 == 'X') or (p1 == 'C' and p2 == 'Y')):
            # Case: Loss
            return 0
        elif ((p1 == 'A' and p2 == 'Y') or (p1 == 'B' and p2 == 'Z') or (p1 == 'C' and p2 == 'X')):
            # Case: Win
            return 6
        # Case: Tie
        return 3
    return sum([ \
        # Adds the value of the shape
        {'X': 1, 'Y': 2, 'Z': 3}[line.split()[1]] + \
        # Adds the score of the match
        score(line.split()) for line in lines])
print (part1())
# submit(part1())
#############################
def part2():
    def shape_score(match):
        p1, cond = match[0], match[1]
        if ((p1 == 'A' and cond == 'Z') or (p1 == 'B' and cond == 'Y') or (p1 == 'C' and cond == 'X')):
            # Case: Need to return Paper
            return 2
        elif ((p1 == 'A' and cond == 'Y') or (p1 == 'B' and cond == 'X') or (p1 == 'C' and cond == 'Z')):
            # Case: Need to return Rock
            return 1
        # Case: Need to return Scissors
        return 3
    return sum([ \
        # Here the second character corresponds to the outcome. So we know what it will result in.
        {'X': 0, 'Y': 3, 'Z': 6}[line.split()[1]] + \
        # The score function now returns the shape score of the shape corresponding to
        # the desired outcome
        shape_score(line.split()) for line in lines])
print(part2())
# submit(part2())
