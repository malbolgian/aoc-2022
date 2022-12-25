def parse_input(input_path: str) -> tuple[tuple[int, int], tuple[int, int], dict[tuple[int, int], int]]:
    with open(input_path, 'r') as f:
        data = f.read().strip().split()
        grid = {}
        for i in range(len(data)):
            if 'S' in data[i]:
                start = (i, data[i].index('S'))
            if 'E' in data[i]:
                end = (i, data[i].index('E'))
            for j in range(len(data[i])):
                grid[(i, j)] = ord(data[i][j]) - 97
        grid[start] = 0
        grid[end] = 25
        return start, end, grid

def valid(pos: tuple[int, int], grid: dict[tuple[int, int], int], seen: set[tuple[int, int]], forward: bool) -> list[tuple[int, int]]:
    points = []
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    for d in dirs:
        point = (pos[0] + d[0], pos[1] + d[1])
        if forward:
            if (point in grid) and (point not in seen) and (grid[point] - grid[pos] <= 1):
                points.append(point)
        else:
            if (point in grid) and (point not in seen) and (grid[pos] - grid[point] <= 1):
                points.append(point)
    return points

def part1(data: tuple[tuple[int, int], tuple[int, int], dict[tuple[int, int], int]]) -> int:
    start, end, grid = data
    seen = set()
    queue = [(start, 0)]
    # BFS from S to E
    while len(queue) > 0:
        pos, dist = queue.pop(0)
        if pos == end:
            return dist
        if pos in seen:
            continue
        seen.add(pos)
        for point in valid(pos, grid, seen, True):
            queue.append((point, dist + 1))
    return -1

def part2(data: tuple[tuple[int, int], tuple[int, int], dict[tuple[int, int], int]]) -> int:
    start, end, grid = data
    seen = set()
    queue = [(end, 0)]
    # BFS from E to any 'a'
    while len(queue) > 0:
        pos, dist = queue.pop(0)
        if grid[pos] == 0:
            return dist
        if pos in seen:
            continue
        seen.add(pos)
        for point in valid(pos, grid, seen, False):
            queue.append((point, dist + 1))
    return -1

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day12.txt')))
    print ('Part Two:', part2(parse_input('input/day12.txt')))
