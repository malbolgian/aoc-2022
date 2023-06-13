def parse_input(input_path: str) -> list[str]:
    with open(input_path, 'r') as f:
        return f.read().strip().split('\n')

def snafu2int(inp: str) -> int:
    total = 0
    power = 1
    least_sig = inp[::-1]
    for i in range(len(inp)):
        total += (('=-012'.index(least_sig[i]) - 2) * power)
        power *= 5
    return total

def int2snafu(num: int) -> str:
    least_sig = ''
    while num > 0:
        least_sig += '012=-'[num % 5]
        num = (num + 2) // 5
    return least_sig[::-1]

def part1(data: list[str]) -> str:
    total = 0
    for snafu in data:
        total += snafu2int(snafu)
    return int2snafu(total)

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day25.txt')))
