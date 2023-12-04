import re
from aocd import lines, submit


def solve(part_no):
    def generate_valve_sequences(pos, open_valves, time_left):
        for nxt in notable_valves:
            if nxt not in open_valves and distances[(pos, nxt)] < time_left:
                # we rule out sequences that will take up more time than we have.
                open_valves.append(nxt)
                yield from generate_valve_sequences(nxt, open_valves, time_left - distances[(pos, nxt)] - 1)
                open_valves.pop()
        yield list(open_valves)

    def get_score(valve_sequence, time_left):
        prv, total = "AA", 0
        for cur in valve_sequence:
            time_left -= distances[(prv, cur)] + 1
            total += valves[cur] * time_left
            prv = cur
        return total

    total_time = {1: 30, 2: 26}[part_no]
    valves = {}
    distances = {}
    for line in lines:  # get valve pressures, get all edges into distances for Floyd Warshall
        codes = re.findall(r'[A-Z]{2}', line)
        distances[(codes[0], codes[0])] = 0
        valves[codes[0]] = int(re.findall(r'\d+', line)[0])
        for adj in codes[1:]:
            distances[(codes[0], adj)] = 1  # Sets codes to 1 for edges
    for i in valves:  # Adds temp infinite distance for vertices without edges
        for j in valves:
            if (i, j) not in distances:
                distances[(i, j)] = float('inf')
    for k in valves:  # Main step of algorithm - updates all shortest paths. O(V3).
        for i in valves:
            for j in valves:
                if distances[(i, j)] > distances[(i, k)] + distances[(k, j)]:
                    distances[(i, j)] = distances[(i, k)] + distances[(k, j)]
    notable_valves = {v: valves[v] for v in valves if valves[v] > 0}

    if part_no == 1:
        best = 0
        for seq in generate_valve_sequences("AA", [], total_time):
            best = max(best, get_score(seq, total_time))

    elif part_no == 2:  # We can maximize by checking the best possible scores for each set of visited
        # Notable valves. We update this by sorting the hash and putting it in the dictionary.
        scores_by_hash = {}
        for seq in generate_valve_sequences("AA", [], total_time):
            score = get_score(seq, total_time)
            hashable = tuple(sorted(seq))
            curr = 0 if not (hashable in scores_by_hash) else scores_by_hash[hashable]
            scores_by_hash[hashable] = max(score, curr)
        scores_by_hash = list(scores_by_hash.items())
        best = 0
        for elf_seq, elf_score in scores_by_hash:
            for phant_seq, phant_score in scores_by_hash:
                # We update the best score only if the elephant and the elf are not intersecting, since that's a waste.
                if set(elf_seq).intersection(set(phant_seq)) == set([]):
                    best = max(best, elf_score + phant_score)

    return best


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
