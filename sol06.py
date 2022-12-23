def parse_input(input_path: str) -> str:
    with open(input_path, 'r') as f:
        return f.read().strip()

def part1(data: str) -> int:
    for i in range(len(data)-3):
        if len(set(data[i:i+4])) == 4:
            return i+4
    return -1

def part2(data: str) -> int:
    for i in range(len(data)-13):
        if len(set(data[i:i+14])) == 14:
            return i+14
    return -1

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day06.txt')))
    print ('Part Two:', part2(parse_input('input/day06.txt')))
