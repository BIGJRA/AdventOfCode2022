from aocd import lines, submit
from collections import deque, defaultdict


def solve(part_no):
    # helper to move blizzards.
    v_add_mod = lambda v1, v2, modx, mody: tuple([(v1[0] + v2[0]) % modx, (v1[1] + v2[1]) % mody])

    def generate_moves(curr_pos):
        # helper to generate tiles you can move (or wait) from position. ignores blizzards here.
        i, j = curr_pos
        yield i, j  # we can always wait
        if curr_pos == start:  # if on start we can only move down
            yield i, j + 1
            return
        elif curr_pos == end:  # if on end we can only move down
            yield end[0], end[1] - 1
            return
        elif curr_pos == (end[0], end[1] - 1):  # special case is when we can move onto end
            yield end
        elif curr_pos == (start[0], start[1] + 1):  # special case is when we can move onto start
            yield start
        if i > 0:
            yield i - 1, j
        if j > 0:
            yield i, j - 1
        if i < c - 1:
            yield i + 1, j
        if j < r - 1:
            yield i, j + 1

    r, c = len(lines) - 2, len(lines[0]) - 2

    # I opted to ignore the walls and just keep track of blizzards and your position.
    # Start and end are 'special cases' so I assign them here
    start, end = (0, -1), (c - 1, r)

    # Keep track of destinations to align with part 2
    destinations = [end]
    if part_no == 2:
        destinations.extend([start, end])

    moves = {'v': (0, 1), '^': (0, -1), '>': (1, 0), '<': (-1, 0)}
    blizzards = defaultdict(list)

    for y, line in enumerate(lines):
        if y == 0 or y == r + 1:  # skip wall rows and cols
            continue
        for x, char in enumerate(line):
            if x == 0 or x == c + 1:
                continue
            if char != '.':
                # data structure here keeps blizzard tiles as keys and a list of
                # blizzard directions as the direction character. Helps with checking collisions.
                blizzards[(x - 1, y - 1)].append(char)

    # state: (current_pos, current_time, remaining destinations). NOTE state of blizzards is constant over t
    queue = deque([(start, 1, destinations)])

    time_max = 0
    while queue:
        curr, t, dest = queue.popleft()
        if t > time_max:  # we can do a lot of processing per minute for the BFS once - here it is

            # set to keep track of all positions (identical state) found during this minute
            s = set([])

            # gets the next set of blizzards
            new = defaultdict(list)
            for pos, dirs in blizzards.items():
                x, y = pos
                for arrow in dirs:
                    nxt = v_add_mod((x, y), moves[arrow], c, r)  # handles mod logic @ walls
                    new[(nxt[0], nxt[1])].append(arrow)
            blizzards = new

            time_max = t  # ends per-minute processing

        for pos in generate_moves(curr):
            if pos == dest[0]:  # this means we hit our next destination
                dest = list(dest[1:])
                if len(dest) == 0:
                    return t  # returns if exhausted all destinations

                # Visiting a destination later is equivalent to reaching it at the
                # earliest possible point and waiting there until the later point,
                # so we can assume WLOG that the only state needed going forward is
                # that of reaching the destination at this earliest possible time.
                # so, we prune all but this state in the queue.
                queue = deque([(pos, t + 1, dest)])

            elif pos not in s and pos not in blizzards:
                # otherwise, we note that we found the pos during the minute, and...
                s.add(pos)
                # add this state to the queue for BFS next minute
                queue.append((pos, t + 1, dest))


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
