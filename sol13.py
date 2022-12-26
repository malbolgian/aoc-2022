from functools import cmp_to_key

def parse_input(input_path: str) -> list[list[str]]:
    with open(input_path, 'r') as f:
        return [line.split('\n') for line in f.read().strip().split('\n\n')]

# Custom comparator for Part 2; returns -1 if in order, 1 if not, and 0 if equivalent
def compare(l, r) -> int:
    if isinstance(l, int) and isinstance(r, int):
        if l < r:
            return -1
        if l == r:
            return 0
        return 1
    
    if isinstance(l, list) and isinstance(r, list):
        for i in range(min(len(l), len(r))):
            result = compare(l[i], r[i])
            if result:
                return result
        return compare(len(l), len(r))
    
    if isinstance(l, int):
        l = [l]
    else:
        r = [r]
    return compare(l, r)

def part1(data: list[list[str]]) -> int:
    out = 0
    for i in range(len(data)):
        if compare(eval(data[i][0]), eval(data[i][1])) == -1:
            out += (i + 1)
    return out

def part2(data: list[list[str]]) -> int:
    packets = [[[2]], [[6]]]
    for pair in data:
        packets.append(eval(pair[0]))
        packets.append(eval(pair[1]))
    packets.sort(key = cmp_to_key(compare))
    return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day13.txt')))
    print ('Part Two:', part2(parse_input('input/day13.txt')))
