def parse_input(input_path: str) -> list[list[int]]:
    with open(input_path, 'r') as f:
        return [[int(i) for i in list(line)] for line in f.read().split()]

def part1(data: list[list[int]]) -> int:
    rows = len(data)
    cols = len(data[0])
    total = 2 * rows + 2 * cols - 4 # Edge trees all visible

    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            tree = data[row][col]
            l = data[row][:col]
            r = data[row][col+1:]
            u = [data[i][col] for i in range(row)]
            d = [data[i][col] for i in range(row+1, rows)]
            if tree > min(max(l), max(r), max(u), max(d)):
                total += 1
    return total

def vision(tree: int, view: list[int]) -> int:
    score = 0
    for height in view:
        score += 1
        if height >= tree:
            break
    return score

def part2(data: list[list[int]]) -> int:
    rows = len(data)
    cols = len(data[0])
    sscore = 0

    # All edge trees have a scenic score of 0
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            tree = data[row][col]
            l = data[row][:col][::-1]
            r = data[row][col+1:]
            u = [data[i][col] for i in range(row-1, -1, -1)]
            d = [data[i][col] for i in range(row+1, rows)]
            score = vision(tree, l) * vision(tree, r) * vision(tree, u) * vision(tree, d)
            if score > sscore:
                sscore = score
    return sscore

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day08.txt')))
    print ('Part Two:', part2(parse_input('input/day08.txt')))
