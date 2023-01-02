def parse_input(input_path: str) -> set[tuple[int, int, int]]:
    with open(input_path, 'r') as f:
        lines = f.read().strip().split('\n')
        return set(tuple(int(i) for i in line.split(',')) for line in lines)

ADJ = {(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)}

def total_area(points: set[tuple[int, int, int]]) -> int:
    area = 0
    for point in points:
        for d in ADJ:
            if (point[0] + d[0], point[1] + d[1], point[2] + d[2]) not in points:
                area += 1
    return area

def part1(data: set[tuple[int, int, int]]) -> int:
    return total_area(data)

def part2(data: set[tuple[int, int, int]]) -> int:
    # Create bounding box with 1-cube buffer so outside air is contiguous
    min_coord = min(min(coord) for coord in data) - 1
    max_coord = max(max(coord) for coord in data) + 1
    in_bounds = lambda tup: all(min_coord <= coord <= max_coord for coord in tup)
    air = set()
    for i in range(min_coord, max_coord + 1):
        for j in range(min_coord, max_coord + 1):
            for k in range(min_coord, max_coord + 1):
                if (i, j, k) not in data:
                    air.add((i, j, k))
    # After we finish expanding, air only contains enclosed cubes
    queue = {(min_coord, min_coord, min_coord)}
    while len(queue) > 0:
        point = queue.pop()
        air.remove(point)
        for d in ADJ:
            new_point = (point[0] + d[0], point[1] + d[1], point[2] + d[2])
            if (new_point in air) and in_bounds(new_point):
                queue.add(new_point)
    return total_area(data) - total_area(air)

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day18.txt')))
    print ('Part Two:', part2(parse_input('input/day18.txt')))
