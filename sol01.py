def parse_input(input_path: str) -> list[list[int]]:
    with open(input_path, 'r') as f:
        elves = f.read().split('\n\n')
        return [[int(cal) for cal in elf.split()] for elf in elves]

def part1(data: list[list[int]]) -> int:
    totals = [sum(elf) for elf in data]
    return max(totals)

def part2(data: list[list[int]]) -> int:
    totals = [sum(elf) for elf in data]
    return sum(sorted(totals, reverse=True)[:3])

if __name__ == '__main__':
    input_data = parse_input('input/day01.txt')
    print ('Part One:', part1(input_data))
    print ('Part Two:', part2(input_data))
