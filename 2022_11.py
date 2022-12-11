from aocd import lines, submit
from collections import deque
from math import gcd


def solve(part_no):
    monkeys = []
    mod_lcm = 1

    def lcm(num1, num2):
        return abs(num1 * num2) // gcd(num1, num2)

    def extract_function(sub):
        left, operation, right = sub.split()
        if left == right and operation == '*':
            return lambda old: old ** 2
        elif operation == '+':
            return lambda old: old + int(right)
        elif operation == '*':
            return lambda old: old * int(right)

    for line in lines:
        if 'Monkey ' in line:
            monkeys.append({'items': deque([]), 'counted': 0, 'targets': [-1, -1]})
        elif 'Starting' in line:
            monkeys[-1]['items'].extend([int(x) for x in (line.split(': ')[1]).split(', ')])
        elif 'Operation' in line:
            monkeys[-1]['operation'] = extract_function(line.split(' = ')[1])
        elif 'Test' in line:
            monkeys[-1]['mod'] = int(line.split(' by ')[1])
            mod_lcm = lcm(monkeys[-1]['mod'], mod_lcm)
        elif 'If ' in line:  # Targets array is [If False, If True]
            monkeys[-1]['targets'][int('true' in line)] = int(line.split(' monkey ')[1])
    for dummy_round in range({1: 20, 2: 10000}[part_no]):
        for monkey in monkeys:
            while monkey['items']:
                monkey['counted'] += 1
                item = monkey['items'].popleft()
                item = monkey['operation'](item)
                if part_no == 1:
                    item //= 3
                monkeys[monkey['targets'][item % monkey['mod'] == 0]]['items'].append(item % mod_lcm)
    counted_list = sorted([monkey['counted'] for monkey in monkeys], reverse=True)
    return counted_list[0] * counted_list[1]


p1 = solve(1)
assert p1 == (113220)
print(p1)
# submit(p1)

p2 = solve(2)
assert p2 == (30599555965)
print(p2)
# submit(p2)
