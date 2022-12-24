def parse_input(input_path: str) -> list[tuple[str, int]]:
    with open(input_path, 'r') as f:
        return [(line[0], int(line[2:])) for line in f.read().strip().split('\n')]

def step(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    if abs(head[0] - tail[0]) == 2 or abs(head[1] - tail[1]) == 2:
        if head[0] > tail[0]:
            tail = (tail[0] + 1, tail[1])
        elif head[0] < tail[0]:
            tail = (tail[0] - 1, tail[1])
        if head[1] > tail[1]:
            tail = (tail[0], tail[1] + 1)
        elif head[1] < tail[1]:
            tail = (tail[0], tail[1] - 1)
    return tail

def part1(data: list[tuple[str, int]]) -> int:
    head = (0, 0)
    tail = (0, 0)
    tailset = set()
    dirs = {'L': (-1, 0), 'R': (1, 0), 'U': (0, 1), 'D': (0, -1)}
    for line in data:
        d = dirs[line[0]]
        for i in range(line[1]):
            head = (head[0] + d[0], head[1] + d[1])
            tail = step(head, tail)
            tailset.add(tail)
    return len(tailset)

def part2(data: list[tuple[str, int]]) -> int:
    NUM_KNOTS = 10
    knots = [(0, 0)] * NUM_KNOTS
    tailset = set()
    dirs = {'L': (-1, 0), 'R': (1, 0), 'U': (0, 1), 'D': (0, -1)}
    for line in data:
        d = dirs[line[0]]
        for i in range(line[1]):
            knots[0] = (knots[0][0] + d[0], knots[0][1] + d[1])
            for j in range(1, NUM_KNOTS):
                knots[j] = step(knots[j-1], knots[j])
            tailset.add(knots[-1])
    return len(tailset)

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day09.txt')))
    print ('Part Two:', part2(parse_input('input/day09.txt')))
