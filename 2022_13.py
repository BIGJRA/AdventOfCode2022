from aocd import lines, submit
from functools import cmp_to_key


def solve(part_no):
    def compare_lists(list1, list2):  # takes two lists as input
        # outputs 1 if they are in the right order
        # outputs -1 if they are not in the right order
        # outputs 0 if both lists are the same
        for idx in range(len(list1)):
            curr1 = list1[idx]
            try:
                curr2 = list2[idx]
            except IndexError:
                return -1
            if type(curr1) == int and type(curr2) == int:
                if curr1 < curr2:
                    return 1
                if curr1 > curr2:
                    return -1
            else:
                if type(curr1) == list and type(curr2) == list:
                    outcome = compare_lists(curr1, curr2)
                elif type(curr2) == list:
                    outcome = compare_lists([curr1], curr2)
                elif type(curr1) == list:
                    outcome = compare_lists(curr1, [curr2])
                if outcome in [-1, 1]:
                    return outcome
        if len(list1) < len(list2):
            return 1
        return 0

    if part_no == 1:
        compare = []
        idx = 1
        total = 0
        for line in lines:
            if line == '':
                outcome = compare_lists(compare[0], compare[1])
                if outcome == 1:
                    total += idx
                idx += 1
                compare = []
            else:
                compare.append(eval(line))
        return total

    if part_no == 2:
        packets = [[[2]], [[6]]]
        for line in set(lines).difference({''}):
            packets.append(eval(line))
        packets = sorted(packets, key=cmp_to_key(compare_lists), reverse=True)
        return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
