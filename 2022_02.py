from aocd import lines, submit


def solve(part_no):
    def get_score(match):
        p1, p2 = match[0], match[1]
        if (p1 == 'A' and p2 == 'Z') or (p1 == 'B' and p2 == 'X') or (p1 == 'C' and p2 == 'Y'):
            return 0  # Case: Loss
        elif (p1 == 'A' and p2 == 'Y') or (p1 == 'B' and p2 == 'Z') or (p1 == 'C' and p2 == 'X'):
            return 6  # Case: Win
        return 3  # Case: Tie

    def get_shape_score(match):
        p1, cond = match[0], match[1]
        if (p1 == 'A' and cond == 'Z') or (p1 == 'B' and cond == 'Y') or (p1 == 'C' and cond == 'X'):
            return 2  # Case: Need to return Paper
        elif (p1 == 'A' and cond == 'Y') or (p1 == 'B' and cond == 'X') or (p1 == 'C' and cond == 'Z'):
            return 1  # Case: Need to return Rock
        return 3  # Case: Need to return Scissors

    if part_no == 1:
        return sum([ \
            # Adds the value of the shape
            {'X': 1, 'Y': 2, 'Z': 3}[line.split()[1]] + \
            # Adds the score of the match
            get_score(line.split()) for line in lines])
    elif part_no == 2:
        return sum([ \
            # Here the second character corresponds to the outcome. So we know what it will result in.
            {'X': 0, 'Y': 3, 'Z': 6}[line.split()[1]] + \
            # The score function now returns the shape score of the shape corresponding to desired outcome.
            get_shape_score(line.split()) for line in lines])


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
