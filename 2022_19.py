from aocd import lines, submit
import re


def solve(part_no):
    def get_blueprints(lines):
        blueprints = []
        for line in lines:
            nums = re.findall(r'\d+', line)
            blueprints.append(tuple([(int(nums[1]), 0, 0, 0),
                                     (int(nums[2]), 0, 0, 0),
                                     (int(nums[3]), int(nums[4]), 0, 0),
                                     (int(nums[5]), 0, int(nums[6]), 0)]))
        return tuple(blueprints)

    def play(blueprint, num_minutes):
        max_geodes = 0

        queue = [(0, (1, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))]
        # States: (minutes_passed, robots, on_hand_resources, all_mined_resources)
        max_minutes_passed = 0

        while len(queue) > 0:
            minutes_passed, robots, resources, mined_resources = queue.pop(0)

            # Prune once per minute
            if minutes_passed > max_minutes_passed:
                # Sorting function just massively favors those that have found more advanced resources
                queue.sort(key=lambda state: sum([state[3][i] * 24 ** i for i in range(4)]), reverse=True)
                queue = queue[:keep]
                max_minutes_passed = minutes_passed

            # Iteration is over - update max geodes
            if minutes_passed == num_minutes:
                max_geodes = max(max_geodes, mined_resources[3])
                continue

            new_resources = tuple([resources[i] + robots[i] for i in range(4)])
            mined_resources = tuple([mined_resources[i] + robots[i] for i in range(4)])

            queue.append((minutes_passed + 1, robots, new_resources, mined_resources))
            for idx, robot_type in enumerate(blueprint):
                if all([robot_type[i] <= resources[i] for i in range(4)]):
                    nxt_resources = tuple([new_resources[i] - robot_type[i] for i in range(4)])
                    nxt_robots = tuple([robots[i] + (i == idx) for i in range(4)])
                    queue.append((minutes_passed + 1, nxt_robots, nxt_resources, mined_resources))
        return max_geodes

    # Too lazy to use logic to prune branches, I just take those with the most 'advanced' resources so far.
    # Can modify how many to keep - too few = less chance of correctness, too many = overtime.
    # Here I just upped it until sample input passed :)
    keep = 8000
    p = get_blueprints(lines)
    if part_no == 2:
        p = p[:3]
    ans = part_no - 1  # P1: 0, P2: 1. for add/mult. Over-engineering???? :)
    for idx, blueprint in enumerate(p):
        mined_geodes = play(blueprint, {1: 24, 2: 32}[part_no])
        if part_no == 1:
            ans += (idx + 1) * mined_geodes
        if part_no == 2:
            ans *= mined_geodes
    return ans


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
