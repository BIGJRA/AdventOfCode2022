from aocd import lines, submit
from collections import deque

def solve(part_no):
    class Room:
        def __init__(self, rock_shapes, jets):
            self.occupied = {}
            self.height = 0
            self.num_rocks = 0

            # Positions to help us place the next rock
            self.rock_idx = 0
            self.rock_shapes = rock_shapes

            # Help us know the next jet in the sequence
            self.jet_idx = 0
            self.jets = jets

            # Used while rock is being placed
            self.current_rock = []

            # Keeps track of things for cycle math
            self.rocks_per_height = []
            self.line_hash = []

        def __str__(self):
            lines = deque()
            lines.appendleft(f'{"-1".ljust(5)}+-------+')
            for y in range(self.height):
                chars = [str(self.occupied[(x, y)]) if (x, y) in self.occupied else '.' for x in range(7)]
                lines.appendleft(f'{str(y).ljust(5)}|{"".join(chars)}|')
            lines.appendleft(f"Room with {self.num_rocks} rocks:")
            return '\n'.join(lines)

        def generate_rock(self):
            pos = self.rock_shapes[self.rock_idx]
            self.current_rock = [(r[0] + 2, r[1] + self.height + 3) for r in pos]
            self.rock_idx += 1
            self.rock_idx %= len(self.rock_shapes)

        def move_rock_horizontally(self):
            drct = 1 if self.jets[self.jet_idx] == '>' else -1
            self.jet_idx += 1
            self.jet_idx %= len(self.jets)
            new = []
            for pos in self.current_rock:
                new_x = pos[0] + drct
                if (new_x, pos[1]) in self.occupied or new_x < 0 or new_x > 6:
                    return False  # could not move rock
                new.append((new_x, pos[1]))
            self.current_rock = new
            return True  # successfully moved rock

        def move_rock_down(self):
            new = []
            for pos in self.current_rock:
                new_y = pos[1] - 1
                if (pos[0], new_y) in self.occupied or new_y < 0:
                    return False  # could not move rock
                new.append((pos[0], new_y))
            self.current_rock = new

            return True  # successfully moved rock

        def drop_rock(self):
            self.generate_rock()
            while True:
                self.move_rock_horizontally()
                moved_down = self.move_rock_down()
                if not moved_down:  # current_rock is in final place. We process other things here.
                    self.num_rocks += 1
                    for settled_rock_pos in self.current_rock:
                        self.occupied[settled_rock_pos] = (self.rock_idx - 1) % 5
                    self.height = max([r[1] for r in self.occupied]) + 1
                    for space in range(len(self.rocks_per_height), self.height):  # Keeps track of how many rocks
                        # exist to get us to a given height. Will be used after finding cycles for ease.
                        try:
                            self.rocks_per_height[space] = self.num_rocks
                        except IndexError:
                            self.rocks_per_height.append(self.num_rocks)
                    for y in range(self.height):  # Adds a bitwise hash of the line to the line_hash.
                        # I use this for cycle finding later on.
                        num = 0
                        for x in range(7):
                            if (x, y) in self.occupied:
                                num += (2 ** x)
                        try:
                            self.line_hash[y] = num
                        except IndexError:
                            self.line_hash.append(num)
                    break

        def check_for_cycle(self):
            CYCLE_SIZE = 50  # I assumed that 50 identical rows-in-a-row would signify a cycle.
            # Higher num == higher accuracy here.
            BUFFER = 5  # To be safe, a buffer of 5 rows helps ensure future blocks will not be discounted.
            # Again, you could increase this buffer to be safe in the case of Tetris I-block drops or something.
            if len(self.line_hash) < CYCLE_SIZE * 3: # To avoid errors I push out the start of checking for cycles.
                return None
            found = False
            end_slice = self.line_hash[-1 * (CYCLE_SIZE + BUFFER):-1 * BUFFER]
            for start in range(len(self.line_hash) - (CYCLE_SIZE + BUFFER) - 1):
                # Sliding window to see if there are any cycles
                start_slice = self.line_hash[start: start + CYCLE_SIZE]
                if start_slice == end_slice:
                    found = True
                    # It's worth noting that this distance may end up a integer multiple of the shortest possible cycle
                    # But this is a non issue since larger cycles are still cycles
                    distance = -1 * (CYCLE_SIZE + BUFFER) + len(self.line_hash) - start
                    break
            if not found:
                return None
            inc = 0
            while self.line_hash[start - inc: start - inc + 50] == self.line_hash[-55 - inc: -5 - inc]:
                inc += 1
            start_index = start - inc + 1
            return distance, start_index

    total_rocks = {1: 2022, 2: 1000000000000}[part_no]
    rock_coords = [
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (0, 1), (1, 1)]]
    directions = lines[0]

    # First we need to find a cycle. To not have to worry about deleting rows or similar, I use a sim first to find the
    # cycle, then get the values needed to solve the problem afterwards.
    sim = Room(rock_coords, directions)
    while sim.num_rocks < total_rocks:
        sim.drop_rock()
        res = sim.check_for_cycle()  # Once a cycle is found we are good
        if res is not None:
            height_per_cycle, height_first_cycle = res
            rocks_at_start = sim.rocks_per_height[height_first_cycle]
            rocks_per_cycle = sim.rocks_per_height[height_first_cycle + height_per_cycle] - rocks_at_start
            remainder_rocks = (total_rocks - rocks_at_start) % rocks_per_cycle
            num_full_cycles = (total_rocks - rocks_at_start) // rocks_per_cycle
            del sim  # delete the unneeded sim object at this point, break the loop
            break

    # Actual room to get the height. It will be just the "before and after" cycle rocks.
    room = Room(rock_coords, directions)
    for rock in range(rocks_at_start + remainder_rocks):
        room.drop_rock()
    return room.height + (num_full_cycles * height_per_cycle) # Cycle rocks are added here


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
