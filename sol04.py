import re

def parse_input(input_path: str) -> list[list[int]]:
    with open(input_path, 'r') as f:
        pairs = f.read().strip().split('\n')
        return [[int(i) for i in re.findall(r'\d+', pair)] for pair in pairs]

def part1(data: list[list[int]]) -> int:
    c = 0
    for pair in data:
        low1, high1, low2, high2 = pair
        if (low1 > low2) or (low1 == low2 and high1 < high2):
            low2, high2, low1, high1 = pair
        if high1 >= high2:
            c += 1
    return c

def part2(data: list[list[int]]) -> int:
    c = 0
    for pair in data:
        low1, high1, low2, high2 = pair
        if (low1 > low2) or (low1 == low2 and high1 < high2):
            low2, high2, low1, high1 = pair
        if high1 >= low2:
            c += 1
    return c

if __name__ == '__main__':
    input_data = parse_input('input/day04.txt')
    print ('Part One:', part1(input_data))
    print ('Part Two:', part2(input_data))
