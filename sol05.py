import re

def parse_input(input_path: str) -> tuple[list[str], list[list[int]]]:
    with open(input_path, 'r') as f:
        start, moves = f.read().split('\n\n')

        # stacks contains initial stack configurations as strings from bottom to top
        stacks = ["" for i in range(9)]
        start = start.split('\n')[:-1][::-1]
        for line in start:
            for stack in range(9):
                if line[stack*4+1] != ' ':
                    stacks[stack] += line[stack*4+1]

        moves = moves.strip().split('\n')
        moves = [[int(i) for i in re.findall(r'\d+', move)] for move in moves]

        return stacks, moves

def part1(data: tuple[list[str], list[list[int]]]) -> str:
    stacks, moves = data
    for move in moves:
        num, src, dst = move
        stacks[dst-1] += stacks[src-1][-num:][::-1]
        stacks[src-1] = stacks[src-1][:-num]
    out = ''
    for stack in stacks:
        out += stack[-1]
    return out

def part2(data: tuple[list[str], list[list[int]]]) -> str:
    stacks, moves = data
    for move in moves:
        num, src, dst = move
        stacks[dst-1] += stacks[src-1][-num:]
        stacks[src-1] = stacks[src-1][:-num]
    out = ''
    for stack in stacks:
        out += stack[-1]
    return out

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day05.txt')))
    print ('Part Two:', part2(parse_input('input/day05.txt')))
