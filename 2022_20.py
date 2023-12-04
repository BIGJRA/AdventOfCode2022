from aocd import lines, submit


def solve(part_no):
    first_entries = lambda array: [num[0] for num in array]
    nums = []
    order = []
    length = len(lines)
    for pos, line in enumerate(lines):
        next_no = int(line)
        if part_no == 2:
            next_no *= 811589153
        nums.append((next_no, pos))
        order.append(next_no)
    num_mixes = {1: 1, 2: 10}[part_no]
    for mix_no in range(num_mixes):
        for order_idx in range(length):
            for mixin_idx in range(length):
                # If the next number in the order matches the next in the mixing bowl, we can now do its movements.
                if nums[mixin_idx][1] == order_idx:
                    curr_num, _ = nums.pop(mixin_idx)
                    # This part was the biggest pain. We need to pop the number we're moving
                    # Which makes kinda a 'ring' of the remaining entries. Then we take the mod of the
                    # moves around this circle (of cycle: length - 1), leading us to where it should go.
                    ftr_pos = (curr_num + mixin_idx) % (length - 1)
                    # note that this makes the position length - 1 "wrap around" to position 0 as intended
                    nums = nums[:ftr_pos] + [(curr_num, order_idx)] + nums[ftr_pos:]
                    break
            # Break brings us back to the order loop, so this begins the next mix operation

    zero_pos = first_entries(nums).index(0)  # looks like 0 is unique... not stated in the problem though.
    return sum([nums[(i + zero_pos) % length][0] for i in range(0, 3001, 1000)])


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
