from aocd import lines, submit
import re


v_add = lambda v1, v2: tuple((v1[i] + v2[i] for i in range(len(v1))))


def solve(part_no, is_sample):
    side = 4 if is_sample else 50 # side size. Could instead be calculated if desired...
    dirs = {'R': (1, 0), 'D': (0, 1), 'L': (-1, 0), 'U': (0, -1)}

    quadrants = [{} for _ in range(6)]
    rows = [[] for _ in range(len(lines[:-2]) // side)]
    cols = [[] for _ in range(max([len(l) for l in lines[:-2]]) // side)]
    y = 0
    q = -1

    curr_pos = None
    curr_dir = 'R' # start going right from first quadrant's top left corner.
    curr_quad = 0
    while y < len(lines) - 2:  # checks each horizontal slice of the map

        line = lines[y]
        d = len(line)
        for block in range(0, d // side):
            if line[block * side] != ' ':  # marks start of block in row
                q += 1  # tracks which quadrants are in which rows/cols
                rows[y // side].append(q)
                cols[block].append(q)
                quadrants[q]['rel_coords'] = (block, y // side) # used to get top left corners later
                # adds all block points to quadrant
                old_y = y
                while y < old_y + side:
                    for x in range(block * side, (block + 1) * side):
                        if curr_pos is None:
                            curr_pos = (x, y)
                        quadrants[q][(x, y)] = lines[y][x]
                    y += 1
                y = old_y
        y = y + side  # update condition to jump to next block

    conns = {}
    if part_no == 1:  # Here we generate the connections by looking at rows and cols
        # print (rows, cols)
        for row in rows: # loops to the left and right for each row
            for pos, quad in enumerate(row):
                conns[(quad, 'R')] = (row[(pos + 1) % len(row)], 'L')
                conns[(quad, 'L')] = (row[(pos - 1) % len(row)], 'R')
        for col in cols:# loops above and below for each column
            for pos, quad in enumerate(col):
                conns[(quad, 'D')] = (col[(pos + 1) % len(col)], 'U')
                conns[(quad, 'U')] = (col[(pos - 1) % len(col)], 'D')
    elif part_no == 2:
        if is_sample:  # Manual for now. Eventually maybe I will change this
            # to intelligently calculate sides for the cube. too much work!
            # These were calculated by looking really hard at a piece of paper.
            conns = {
                (0, 'R'): (5, 'R'), (0, 'D'): (3, 'U'), (0, 'L'): (2, 'U'), (0, 'U'): (1, 'U'),
                (1, 'R'): (2, 'L'), (1, 'D'): (4, 'D'), (1, 'L'): (5, 'D'), (1, 'U'): (0, 'U'),
                (2, 'R'): (3, 'L'), (2, 'D'): (4, 'L'), (2, 'L'): (1, 'R'), (2, 'U'): (0, 'L'),
                (3, 'R'): (5, 'U'), (3, 'D'): (4, 'U'), (3, 'L'): (2, 'R'), (3, 'U'): (0, 'D'),
                (4, 'R'): (5, 'L'), (4, 'D'): (1, 'D'), (4, 'L'): (2, 'D'), (4, 'U'): (3, 'D'),
                (5, 'R'): (0, 'R'), (5, 'D'): (1, 'L'), (5, 'L'): (4, 'R'), (5, 'U'): (3, 'R')}
        else:
            conns = {
                (0, 'R'): (1, 'L'), (0, 'D'): (2, 'U'), (0, 'L'): (3, 'L'), (0, 'U'): (5, 'L'),
                (1, 'R'): (4, 'R'), (1, 'D'): (2, 'R'), (1, 'L'): (0, 'R'), (1, 'U'): (5, 'D'),
                (2, 'R'): (1, 'D'), (2, 'D'): (4, 'U'), (2, 'L'): (3, 'U'), (2, 'U'): (0, 'D'),
                (3, 'R'): (4, 'L'), (3, 'D'): (5, 'U'), (3, 'L'): (0, 'L'), (3, 'U'): (2, 'L'),
                (4, 'R'): (1, 'R'), (4, 'D'): (5, 'R'), (4, 'L'): (3, 'R'), (4, 'U'): (2, 'D'),
                (5, 'R'): (4, 'D'), (5, 'D'): (1, 'U'), (5, 'L'): (0, 'U'), (5, 'U'): (3, 'D')}

    moves = re.findall(r'\d+|L|R', lines[-1])
    for move in moves:
        # updates current direction if given L or R
        if move == 'R':
            curr_dir = {"R": "D", "D": "L", "L": "U", "U": "R"}[curr_dir]
        elif move == 'L':
            curr_dir = {"R": "U", "U": "L", "L": "D", "D": "R"}[curr_dir]

        else:
            num_moves = int(move)
            for _ in range(num_moves):
                x, y = curr_pos
                nxt_pos = v_add(curr_pos, dirs[curr_dir])
                if nxt_pos not in quadrants[curr_quad]:
                    nxt_quad, nxt_dir = conns[(curr_quad, curr_dir)]
                    if curr_dir == "R":  # checks for which way you're 'leaving' to see how far you are
                        edge_idx = y % side
                    elif curr_dir == "L":
                        edge_idx = (-y - 1) % side
                    elif curr_dir == "U":
                        edge_idx = x % side
                    elif curr_dir == "D":
                        edge_idx = (-x - 1) % side
                    # figures out how far from the left corner looking out you are, then switches
                    # to how far from the right corner looking in you are to match up.
                    edge_idx = side - edge_idx - 1

                    blocks_x = quadrants[nxt_quad]['rel_coords'][0]
                    blocks_y = quadrants[nxt_quad]['rel_coords'][1]

                    if nxt_dir == "R":  # takes the side you enter from to calculate next position
                        nxt_pos = blocks_x * side + (side - 1), blocks_y * side + edge_idx
                    elif nxt_dir == "L":
                        nxt_pos = blocks_x * side, blocks_y * side + (side - 1) - edge_idx
                    elif nxt_dir == "U":
                        nxt_pos = blocks_x * side + edge_idx, blocks_y * side
                    elif nxt_dir == "D":
                        nxt_pos = blocks_x * side + (side - 1) - edge_idx, blocks_y * side + (side - 1)

                    # Updates nxt_dir to go inwards at new quadrant
                    nxt_dir = {"R": "L", "D": "U", "U": "D", "L": "R"}[nxt_dir]
                else:
                    nxt_quad = curr_quad
                    nxt_dir = curr_dir
                if quadrants[nxt_quad][nxt_pos] == '#':
                    break
                else:
                    curr_dir, curr_pos, curr_quad = nxt_dir, nxt_pos, nxt_quad
    return 1000 * (curr_pos[1] + 1) + 4 * (curr_pos[0] + 1) + ["R", "D", "L", "U"].index(curr_dir)


p1 = solve(1, False)
print(p1)
# submit(p1)

p2 = solve(2, False)
print(p2)
# submit(p2)
