from aocd import lines, submit
import re
from functools import lru_cache

lines = '''Blueprint 1:Each ore robot costs 4 ore.Each clay robot costs 2 ore.Each obsidian robot costs 3 ore and 14 clay.Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2:Each ore robot costs 2 ore.Each clay robot costs 3 ore.Each obsidian robot costs 3 ore and 8 clay.Each geode robot costs 3 ore and 12 obsidian.'''.splitlines()

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

    @lru_cache()
    def play(blueprint, min_left, resources, robots):
        if min_left == 0:
            # print(resources, robots)
            return resources[3]
        ret = 0
        for spent, added_robots in generate_buy_options(blueprint, resources):
            ret = max(ret, play(blueprint, min_left - 1,
                 tuple([resources[i] + robots[i] - spent[i] for i in range(4)]),
                 tuple([robots[i] + added_robots[i] for i in range(4)])))
        return ret

    @lru_cache()
    def generate_buy_options(blueprint, resources):
        spent = (0,0,0,0)
        robots = (0,0,0,0)
        yield spent, robots
        for idx, robot_type in enumerate(blueprint):
            if all([robot_type[i] <= resources[i] for i in range(4)]):
                nxt_spent = tuple([spent[i] + robot_type[i] for i in range(4)])
                nxt_robots = tuple([robots[i] + (i == idx) for i in range(4)])
                yield nxt_spent, nxt_robots

    p = get_blueprints(lines)
    m = 0
    for blueprint in p:
        #print (blueprint)
        # score = 0
        sc = play(blueprint, 24, (0, 0, 0, 0), (1, 0, 0, 0))
        #print (sc)
        m += sc
    return m


p1 = solve(1)
print(p1)
# submit(p1)

# p2 = solve(2)
# print(p2)
# submit(p2)
