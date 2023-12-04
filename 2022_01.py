from aocd import lines, submit

def solve(part_no):
    maxes_dict = {1: 1, 2: 3}
    curr_maxes = [0] * maxes_dict[part_no]
    curr_sum = 0
    for line in lines:
        if line == '':
            curr_maxes = sorted(curr_maxes + [curr_sum], reverse=True)[:maxes_dict[part_no]]
            curr_sum = 0
        elif line != '':
            curr_sum += int(line)
    return sum(curr_maxes)

p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)

