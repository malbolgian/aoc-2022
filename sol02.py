def parse_input(input_path: str) -> list[list[str]]:
    with open(input_path, 'r') as f:
        rounds = f.read().strip().split('\n')
        return [r.split() for r in rounds]

def part1(data: list[list[str]]) -> int:
    rep = ['A', 'B', 'C', '', 'X', 'Y', 'Z'] # convoluted representation to simplify calculation
    score = 0
    for opp, you in data:
        score += (rep.index(you) - 3) # individual score
        score += 3 * ((rep.index(you) - rep.index(opp)) % 3) # matchup score
    return score

def part2(data: list[list[str]]) -> int:
    score = 0
    for opp, you in data:
        score += ((ord(opp) + ord(you) - 1) % 3 + 1) # individual score
        score += 3 * ((ord(you) - 1) % 3) # matchup score
    return score

if __name__ == '__main__':
    input_data = parse_input('input/day02.txt')
    print ('Part One:', part1(input_data))
    print ('Part Two:', part2(input_data))
