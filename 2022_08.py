from aocd import lines, submit


def solve(part_no):
    m, n = len(lines), len(lines[0])
    if part_no == 1:
        visible_coords = set([])
        m, n = len(lines), len(lines[0])
        for i in range(m):
            left_curr = right_curr = -1
            for j in range(n):
                height = int(lines[i][j])
                if height > left_curr:
                    visible_coords.add((i, j))
                    left_curr = height
            for j in range(n - 1, -1, -1):
                height = int(lines[i][j])
                if height > right_curr:
                    visible_coords.add((i, j))
                    right_curr = height
        for j in range(n):
            top_curr = bottom_curr = -1
            for i in range(m):
                height = int(lines[i][j])
                if height > top_curr:
                    visible_coords.add((i, j))
                    top_curr = height
            for i in range(m - 1, -1, -1):
                height = int(lines[i][j])
                if height > bottom_curr:
                    visible_coords.add((i, j))
                    bottom_curr = height
        return len(list(visible_coords))
    elif part_no == 2:
        best_mult = 0
        for i in range(1, m - 1):
            for j in range(1, n - 1):
                curr_tree_height = lines[i][j]
                curr_mult = 1
                total_per_dir = 0

                left_idx = i - 1
                right_idx = i + 1
                top_idx = j - 1
                bottom_idx = j + 1

                while left_idx >= 0:
                    total_per_dir += 1
                    next_tree_height = lines[left_idx][j]
                    if next_tree_height >= curr_tree_height:
                        break
                    left_idx -= 1
                curr_mult *= total_per_dir
                total_per_dir = 0

                while right_idx <= m - 1:
                    total_per_dir += 1
                    next_tree_height = lines[right_idx][j]
                    if next_tree_height >= curr_tree_height:
                        break
                    right_idx += 1
                curr_mult *= total_per_dir
                total_per_dir = 0

                while top_idx >= 0:
                    total_per_dir += 1
                    next_tree_height = lines[i][top_idx]
                    if next_tree_height >= curr_tree_height:
                        break
                    top_idx -= 1
                curr_mult *= total_per_dir
                total_per_dir = 0

                while bottom_idx <= n - 1:
                    total_per_dir += 1
                    next_tree_height = lines[i][bottom_idx]
                    if next_tree_height >= curr_tree_height:
                        break
                    bottom_idx += 1
                curr_mult *= total_per_dir

                best_mult = max(best_mult, curr_mult)
        return best_mult


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
