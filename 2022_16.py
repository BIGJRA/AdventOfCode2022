import re
from functools import *
from aocd import lines, submit
import itertools
from dataclasses import dataclass

linesf = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''.splitlines()

# @dataclass
# class Valve:
#     name: str
#     flow_rate: int
#     children: list[str]

# ('DD', 'BB', 'JJ', 'HH', 'EE', 'CC')
def solve(part_no):

    @lru_cache()
    def dp(valve, visited, ppm, total_pressure, minutes, path):
        nonlocal best
        #print(valve, ppm, total_pressure, minutes, path)

        if minutes >= total_time:
            # print(valve, ppm, total_pressure, minutes, path)
            best = max(best, total_pressure)
            return best
        visited = visited.union(frozenset([valve]))
        minutes = minutes + 1
        total_pressure += ppm
        ppm += valves[valve]
        path = path + (valve,)
        # print(valve, ppm, total_pressure, minutes, path)

        # print(valve, ppm, total_pressure, minutes, path)
        for adj in valves:
            if adj not in visited:
                d = distances[(valve, adj)]
                to_add = (ppm * min(d, total_time - minutes))
                dp(adj, visited, ppm, total_pressure + to_add, min(total_time, minutes + d), path)
        if sorted(valves.keys()) == sorted(list(visited)):
            dp(adj, visited, ppm, total_pressure + (total_time - minutes) * ppm, total_time, path)

    total_time = {1:30,2:26}[part_no]
    valves = {}
    distances = {}
    for line in lines: # get valve pressures, get all edges into distances for Floyd Warshall
        codes = re.findall(r'[A-Z]{2}', line)
        distances[(codes[0],codes[0])] = 0
        valves[codes[0]] = int(re.findall(r'\d+', line)[0])
        for adj in codes[1:]:
            distances[(codes[0], adj)] = 1 # Sets codes to 1 for edges
    for i in valves: # Adds temp infinite distance for vertices without edges
        for j in valves:
            if (i, j) not in distances:
                distances[(i, j)] = float('inf')
    for k in valves: # Main step of algorithm - updates all shortest paths. O(V3).
        for i in valves:
            for j in valves:
                if distances[(i, j)] > distances[(i, k)] + distances[(k, j)]:
                    distances[(i, j)] = distances[(i, k)] + distances[(k, j)]

    to_del = []
    for valve, pressure in valves.items(): # Takes out the non-useful valve pressures.
        if pressure == 0:
            to_del.append(valve)
    for del_valve in to_del:
        del valves[del_valve]
    #print (distances)
    #print (valve_pressures)
    best = 0
    for valve in valves:
        dp(valve, frozenset(), 0, 0, distances[('AA', valve)], ())
    return best


p1 = solve(1)
print(p1)
# submit(p1)

# p2 = solve(2)
# print(p2)
# submit(p2)

def solve2(part_no):

    def calculate_total_pressure(order):
        #print (order)
        time = 0
        idx = -1
        prv = 'AA'
        cur = order[0]
        ppm = 0
        total = 0
        while time < 30:
            idx += 1
            if idx == len(order):
                move_time = 30 - time
                total += (ppm * move_time)
                time = 30
                print(time, idx, prv, cur, ppm, total)
                return total
            cur = order[idx]
            #print (time, prv, cur, ppm, total)
            d = distances[(prv, cur)]
            move_time = min(d, 30 - time)
            total += ppm * move_time
            time += move_time
            if time < 30:
                prv = cur
                move_time = 1
                total += (ppm * move_time)
                time += move_time
                ppm += valve_pressures[cur]
                #print(time, prv, cur, ppm, total)
            prv = cur
        #print(time, prv, cur, ppm, total)
        return total

    valve_pressures = {}
    distances = {}
    for line in lines: # get valve pressures, get all edges into distances for Floyd Warshall
        codes = re.findall(r'[A-Z]{2}', line)
        distances[(codes[0],codes[0])] = 0
        valve_pressures[codes[0]] = int(re.findall(r'\d+', line)[0])
        for adj in codes[1:]:
            distances[(codes[0], adj)] = 1 # # S
    for i in valve_pressures: # Adds temp infinite distance for vertices without edges
        for j in valve_pressures:
            if (i, j) not in distances:
                distances[(i, j)] = float('inf')
    for k in valve_pressures: # Main step of algorithm - updates all shortest paths. O(V3).
        for i in valve_pressures:
            for j in valve_pressures:
                if distances[(i, j)] > distances[(i, k)] + distances[(k, j)]:
                    distances[(i, j)] = distances[(i, k)] + distances[(k, j)]

    to_del = []
    for valve, pressure in valve_pressures.items(): # Takes out the non-useful valve pressures.
        if pressure == 0:
            to_del.append(valve)
    print (valve_pressures)

    for del_valve in to_del:
        del valve_pressures[del_valve]
    #print (distances)
    print (valve_pressures)
    best = 0
    for perm in itertools.permutations(valve_pressures.keys()):
        best = max(best, calculate_total_pressure(perm))
    return best

#p1 = solve2(1)
#print(p1)
# submit(p1)


