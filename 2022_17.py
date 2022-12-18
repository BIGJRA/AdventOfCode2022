from aocd import lines, submit
from collections import deque
import math

lifnes = '''>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'''.splitlines()

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

            # Once cycle is found we use these to do the iteration work
            self.found = False
            self.cycle_start = 0
            self.cycle_length = 0

        def get_height(self):
            return self.height

        def add_height(self, height):
            self.height += height

        def add_rocks(self, num_rocks):
            self.num_rocks += num_rocks

        def get_num_rocks(self):
            return self.num_rocks

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
            # print ("before horz", self.current_rock, drct)
            for pos in self.current_rock:
                new_x = pos[0] + drct
                if (new_x, pos[1]) in self.occupied or new_x < 0 or new_x > 6:
                    # print("after  horz", self.current_rock, False)
                    return False # could not move rock
                new.append((new_x, pos[1]))
            self.current_rock = new
            # print ("after  horz", self.current_rock, True)
            return True # successfully moved rock

        def move_rock_down(self):
            new = []
            # print ("before down", self.current_rock, -1)

            for pos in self.current_rock:
                new_y = pos[1] - 1
                if (pos[0], new_y) in self.occupied or new_y < 0:
                    # print("after  down", self.current_rock, False)
                    return False # could not move rock
                new.append((pos[0], new_y))
            self.current_rock = new
            # print ("after  down", self.current_rock, True)

            return True # successfully moved rock

        def drop_rock(self):
            self.generate_rock()
            while True:
                self.move_rock_horizontally()
                moved_down = self.move_rock_down()
                if not moved_down: # current_rock is in final place.
                    self.num_rocks += 1
                    for settled_rock_pos in self.current_rock:
                        self.occupied[settled_rock_pos] = (self.rock_idx - 1) % 5# once rock is in place, add it to occupied
                    self.height = max([r[1] for r in self.occupied]) + 1
                    for space in range(len(self.rocks_per_height), self.height):
                        try:
                            self.rocks_per_height[space] = self.num_rocks
                        except IndexError:
                            self.rocks_per_height.append(self.num_rocks)
                    for y in range(self.get_height()):
                        num = 0
                        for x in range(7):
                            if (x, y) in self.occupied:
                                num += (2 ** x)
                        try:
                            self.line_hash[y] = num
                        except IndexError:
                            self.line_hash.append(num)
                    # if not self.found:
                    #     self.check_for_cycle()
                    break

        def check_for_cycle(self):

            if len(self.line_hash) < 100:
                return False
            curr = self.line_hash[-55:-5]
            found = False
            for start in range(len(self.line_hash) - 55):
                if self.line_hash[start: start + 50] == curr:
                    found = True
                    distance = -55 + len(self.line_hash) - start
                    break
            if not found:
                return False
            inc = 0
            while self.line_hash[start - inc: start - inc + 50] == self.line_hash[-55 - inc: -5 - inc]:
                inc += 1
            self.found = True
            self.cycle_length = distance
            self.cycle_start = start - inc + 1
            return True

    total_rocks = {1:2022,2:1000000000000}[part_no]
    sim = Room([
        [(0,0),(1,0),(2,0),(3,0)],
        [(0,1),(1,0),(1,1),(1,2),(2,1)],
        [(0,0),(1,0),(2,0),(2,1),(2,2)],
        [(0,0),(0,1),(0,2),(0,3)],
        [(0,0),(1,0),(0,1),(1,1)]], lines[0])
    # print(room)
    broken = False
    while sim.get_num_rocks() < total_rocks:
        sim.drop_rock()
        if not sim.found:
            if sim.check_for_cycle():
                #print (sim.cycle_length, sim.cycle_start)
                height_per_cycle = sim.cycle_length
                cycle_length = sim.rocks_per_height[sim.cycle_start + sim.cycle_length] - sim.rocks_per_height[sim.cycle_start]
                cycle_start = sim.rocks_per_height[sim.cycle_start - 1]
                remaining_rocks = (total_rocks - cycle_start) % cycle_length
                num_cycles = (total_rocks - cycle_start) // cycle_length
                broken = True
                break
                # print (list(enumerate(sim.rocks_per_height)))
                #print (cycle_length, cycle_start, remaining_rocks, num_cycles)
                #print(sim)
            if broken:
                break
        if broken:
            break

    room = Room([
        [(0,0),(1,0),(2,0),(3,0)],
        [(0,1),(1,0),(1,1),(1,2),(2,1)],
        [(0,0),(1,0),(2,0),(2,1),(2,2)],
        [(0,0),(0,1),(0,2),(0,3)],
        [(0,0),(1,0),(0,1),(1,1)]], lines[0])
    for rock in range(cycle_start):
        room.drop_rock()
    #print(room.height)
    for rock in range(remaining_rocks):
        room.drop_rock()
    #print(room.height)
    #print (room)
    room.add_height(num_cycles * height_per_cycle)

    #print(room.height)
    return room.get_height()



p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)