from aocd import lines, submit
import re


def solve(part_no):
    def manhattan_distance(pt1, pt2):
        x1, y1 = pt1
        x2, y2 = pt2
        return abs(y1 - y2) + abs(x1 - x2)

    def find_x_ends(sensor, height, distance):
        x, y = sensor
        stretch = distance - abs(height - y)
        if stretch < 0:
            return None
        return sorted([x - stretch, x + stretch])

    def generate_ring(sensor, radius):
        x, y = sensor
        for step in range(1, radius):
            yield x + step, y + (radius - step)
            yield x + step, y - (radius - step)
            yield x - step, y + (radius - step)
            yield x - step, y - (radius - step)
        yield x + radius, y
        yield x - radius, y
        yield x, y + radius
        yield x, y - radius

    sbd = {}  # Will be in the form {sensor: [beacon, manhattan distance]}
    for line in lines:
        sp = re.split(r'=|,|:', line)
        s = (int(sp[1]), int(sp[3]))
        b = (int(sp[5]), int(sp[7]))
        d = manhattan_distance(s, b)
        sbd[s] = [b, d]
    beacons = set([sbd[s][0] for s in sbd])
    p1_height = 2000000
    p2_bounds = 4000000
    found = set()
    for s, arr in sbd.items():
        b, d = arr
        if part_no == 1:
            x_ends = find_x_ends(s, p1_height, d)
            if x_ends is not None:
                for x in range(x_ends[0], x_ends[1] + 1):
                    if (x, p1_height) not in beacons:
                        found.add((x, p1_height))
        elif part_no == 2:
            for point in generate_ring(s, d + 1):
                if min(point[0], point[1]) < 0 or max(point[0], point[1]) > p2_bounds:
                    continue
                if any([(manhattan_distance(pt1=point, pt2=sensor) <= sbd[sensor][1]) for sensor in sbd.keys()]):
                    continue
                return point[0] * 4000000 + point[1]  # exit once this point is found
    return len(list(found))  # answer for part 1


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
