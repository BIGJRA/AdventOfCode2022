from aocd import lines, submit
from collections import Counter
from copy import deepcopy


def solve(part_no):
    v_add = lambda v1, v2: tuple([v1[i] + v2[i] for i in range(len(v1))])
    extrema = lambda e: tuple([min([elf[0] for elf in e]), max([elf[0] for elf in e]),
                               min([elf[1] for elf in e]), max([elf[1] for elf in e])])

    # Directions are stored as direction to move first, then the places that
    # need to be empty second and third.
    dirs = [[(0, -1), (-1, -1), (1, -1)],  # N, NW, NE
            [(0, 1), (-1, 1), (1, 1)],  # S, SW, SE
            [(-1, 0), (-1, -1), (-1, 1)],  # W, NW, SW
            [(1, 0), (1, -1), (1, 1)]]  # E, NE, SE
    all_dirs = list(set([dirs[i][j] for j in range(3) for i in range(4)]))
    elves = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                elves.append((x, y))

    def simulate_round(round_num):
        nonlocal elves
        idx = (round_num - 1) % 4
        proposed = []

        # Part 1
        elf_set = set(elves)
        for elf in elves:
            if all([v_add(elf, d) not in elf_set for d in all_dirs]):
                proposed.append(elf)
            else:
                count = 0
                while count < 4:
                    curr = (idx + count) % 4
                    if all([v_add(elf, d) not in elf_set for d in dirs[curr]]):
                        proposed.append(v_add(elf, dirs[curr][0]))
                        break
                    count += 1
                if count == 4:
                    proposed.append(elf)

        # Part 2
        c = Counter(proposed)
        for i, pos in enumerate(proposed):
            if c[pos] == 1:
                elves[i] = pos

    if part_no == 1:
        for round in range(1, 11):
            simulate_round(round)

        # counts empty tiles in rectangle
        ext = extrema(elves)
        res = 0
        for y in range(ext[2], ext[3] + 1):
            for x in range(ext[0], ext[1] + 1):
                if (x, y) not in elves:
                    res += 1
        return res

    elif part_no == 2:
        round = 1
        prev = deepcopy(elves)
        while True:
            simulate_round(round)
            eq = True
            for pos in range(len(prev)):
                if prev[pos] != elves[pos]:
                    eq = False
                    break
            if eq:
                return round
            prev = deepcopy(elves)
            round += 1


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
