from aocd import lines, submit

def solve():

    def dec_to_snafu(dec):
        chars = []
        while dec > 0:
            mod_adj = (dec + 2) % 5
            chars.append(['=','-','0','1','2'][mod_adj])
            dec = (dec + 2) // 5
        return ''.join(chars[::-1])

    def snafu_to_dec(snafu):
        dec = 0
        for pwr, char in enumerate(snafu[::-1]):
            dec += ((['=','-','0','1','2'].index(char) - 2) * 5 ** pwr)
        return dec

    return dec_to_snafu(sum([snafu_to_dec(snafu) for snafu in lines]))

p1 = solve()
print(p1)
# submit(p1)
