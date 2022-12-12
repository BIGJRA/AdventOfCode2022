from aocd import lines, submit


def solve(part_no):
    def add_char_to_total(char):
        nonlocal total
        total += (1 + ord(char.lower()) - ord('a') + 26 * (ord(char) < ord('a')))

    def find_common_char(string_list):
        # Finds the common char across string list. Assumes exactly 1 such exists.
        s = set(string_list[0])
        for string in string_list[1:]:
            s = s.intersection(string)
        return list(s)[0]

    total = 0
    if part_no == 1:
        for line in lines:
            add_char_to_total(find_common_char([line[:len(line) // 2], line[len(line) // 2:]]))
    elif part_no == 2:
        counter = 0
        curr = []
        for line in lines:
            if counter == 0:
                if curr:
                    add_char_to_total(find_common_char(curr))
                curr = []
            curr.append(line)
            counter = (counter + 1) % 3
        add_char_to_total(find_common_char(curr))
    return total


p1 = solve(1)
print(p1)
# submit(p1)

p2 = solve(2)
print(p2)
# submit(p2)
