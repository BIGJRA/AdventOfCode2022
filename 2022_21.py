from operator import __add__, __sub__, __mul__, __truediv__
from aocd import lines, submit
import re
import sympy

def solve(part_no):
    class Node:
        def __init__(self, name=None, val=None, left=None, right=None, op=None):
            self.name = name
            self.left = left
            self.right = right
            self.val = val
            self.op = op

    node_lookup = {}
    ops = {'+': __add__, '-': __sub__, '*': __mul__, '/': __truediv__}
    for line in lines:
        monkey_name = line[:4]
        if part_no == 2 and monkey_name == 'humn':
            if monkey_name in node_lookup:
                node_lookup[monkey_name].val = sympy.symbols('x')
            else:
                node_lookup[monkey_name] = Node(monkey_name, sympy.symbols('x'), None, None, None)
        elif len(re.findall(r'\d+', line)) > 0:
            value = int(re.findall(r'\d+', line)[0])
            if monkey_name in node_lookup:
                node_lookup[monkey_name].val = value
            else:
                node_lookup[monkey_name] = Node(monkey_name, value, None, None, None)
        else:
            l_monkey, r_monkey = line[6:10], line[13:17]
            if l_monkey in node_lookup:
                left = node_lookup[l_monkey]
            else:
                left = Node(l_monkey, None, None, None, None)
                node_lookup[l_monkey] = left
            if r_monkey in node_lookup:
                right = node_lookup[r_monkey]
            else:
                right = Node(r_monkey, None, None, None, None)
                node_lookup[r_monkey] = right
            op = ops[line[11]]
            if monkey_name in node_lookup:
                node_lookup[monkey_name].left = left
                node_lookup[monkey_name].right = right
                node_lookup[monkey_name].op = op
            else:
                node_lookup[monkey_name] = Node(monkey_name, None, left, right, op)
    def dfs(node):
        if part_no == 2 and node.name == 'root':
            return int(sympy.solve(dfs(node.left) - dfs(node.right))[0])
        if node.val is not None:
            return node.val
        l = dfs(node.left)
        r = dfs(node.right)
        node.val = node.op(l, r)
        return node.val
    v = dfs(node_lookup['root'])
    return int(v)

p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
