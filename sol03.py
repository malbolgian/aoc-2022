def parse_input(input_path: str) -> list[str]:
    with open(input_path, 'r') as f:
        sacks = f.read().strip().split('\n')
        return sacks

def part1(data: list[str]) -> int:
    prio = 0
    for sack in data:
        comp1, comp2 = sack[:len(sack)//2], sack[len(sack)//2:]
        item = (set(comp1) & set(comp2)).pop()
        prio += (ord(item) - 38 if item.isupper() else ord(item) - 96)
    return prio


def part2(data: list[str]) -> int:
    prio = 0
    for group in range(len(data)//3):
        item = (set(data[group*3]) & set(data[group*3+1]) & set(data[group*3+2])).pop()
        prio += (ord(item) - 38 if item.isupper() else ord(item) - 96)
    return prio

if __name__ == '__main__':
    input_data = parse_input('input/day03.txt')
    print ('Part One:', part1(input_data))
    print ('Part Two:', part2(input_data))
