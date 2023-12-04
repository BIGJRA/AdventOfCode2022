from aocd import lines, submit


def solve(part_no):
    def add_vectors(v1, v2):
        if len(v1) != len(v2):
            return IndexError("Vectors not same length")
        v = []
        for idx in range(len(v1)):
            v.append(v1[idx] + v2[idx])
        return tuple(v)

    def find_group(starting_coord):  # returns -1 if outside, else idx of air pocket it's in
        nonlocal outside, air_pockets
        found = {starting_coord}  # We keep track of what's found to add later for speed.

        def dfs(curr):
            nonlocal found
            for idx, pocket in enumerate(air_pockets):
                # If the point is found in an existing air pocket, we return its index
                if curr in pocket:
                    return idx
            if curr in outside:
                # If the point is found in the set of outside points, we return -1
                return -1
            for dim in range(3):
                # If the point is outside the boundary cube, -1 is returned
                if curr[dim] < extrema[dim][0] or curr[dim] > extrema[dim][1]:
                    return -1
            for off in offsets:
                adj = add_vectors(curr, off)
                if adj in cubes or adj in found:  # only care about new, non-cube points
                    continue
                found.add(adj)
                dfs_outcome = dfs(adj)
                if dfs_outcome is not None:  # Recursive DFS call. If it finds a number on
                    # any neighbors, then that is the correct group for the initial point, too.
                    return dfs_outcome
            # return None is performed otherwise. This happens when DFS is exhaustive w/ no match.

        outcome = dfs(starting_coord)
        # We need to now add the found coordinates to the respective outside/pocket for DFS speed.
        if outcome is None:
            air_pockets.append(found) # New air pocket is found, so we need to return its new index.
            return len(air_pockets) - 1
        if outcome == -1:
            outside = outside.union(found)
        else:
            air_pockets[outcome] = air_pockets[outcome].union(found)
        return outcome

    offsets = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    cubes = set([])
    for line in lines:
        cubes.add(tuple([int(x) for x in line.split(',')]))
    total = 0

    # In order to perform DFS on the set of outside points, we need boundaries.
    # This list contains min and max coords for the cube enclosing all input points.
    extrema = [
        [min([cube[0] for cube in cubes]), max([cube[0] for cube in cubes])],
        [min([cube[1] for cube in cubes]), max([cube[1] for cube in cubes])],
        [min([cube[2] for cube in cubes]), max([cube[2] for cube in cubes])]
    ]

    outside = set([])
    air_pockets = [] # Array of sets

    # To make the boundary checking at the end quicker, we store all adjacent coord tiles that are in
    # Air pockets in a separate set for easy checking at the end.
    relevant_air = set([])

    if part_no == 2:
        for cube in cubes:
            for offset in offsets:
                adj_cube = add_vectors(cube, offset)
                if adj_cube not in cubes:
                    group = find_group(adj_cube)
                    if group >= 0:
                        relevant_air.add(adj_cube)
    for cube in cubes:
        for offset in offsets:
            adj_cube = add_vectors(cube, offset)
            if adj_cube not in cubes and adj_cube not in relevant_air:
                total += 1
    return total


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
