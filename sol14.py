from typing import Optional

def parse_input(input_path: str) -> set[tuple[int, int]]:
    with open(input_path, 'r') as f:
        segments = f.read().strip().split('\n')
        walls = set()
        for s in segments:
            points = s.split(' -> ')
            for i in range(len(points) - 1):
                end1 = eval(points[i])
                end2 = eval(points[i+1])
                if end1[0] == end2[0]:
                    for j in range(min(end1[1], end2[1]), max(end1[1], end2[1]) + 1):
                        walls.add((end1[0], j))
                else:
                    for j in range(min(end1[0], end2[0]), max(end1[0], end2[0]) + 1):
                        walls.add((j, end1[1]))
        return walls

def simulate(pos: tuple[int, int], walls: set[tuple[int, int]], max_depth: int) -> Optional[tuple[int, int]]:
    if pos[1] >= max_depth:
        return None
    for d in [0, -1, 1]:
        next_pos = (pos[0] + d, pos[1] + 1)
        if next_pos not in walls:
            return simulate(next_pos, walls, max_depth)
    return pos

def part1(data: set[tuple[int, int]]) -> int:
    SOURCE = (500, 0)
    max_depth = 0
    sand = 0
    
    for wall in data:
        if wall[1] > max_depth:
            max_depth = wall[1]
    while True:
        sand_pos = simulate(SOURCE, data, max_depth)
        if sand_pos:
            sand += 1
            if sand_pos == SOURCE:
                break
            data.add(sand_pos)
        else:
            break
    return sand

def part2(data: set[tuple[int, int]]) -> int:
    SOURCE = (500, 0)
    max_depth = 0
    sand = 0
    # Add a wall that extends (max_depth + 2) to the left and right of source
    for wall in data:
        if wall[1] > max_depth:
            max_depth = wall[1]
    for i in range(SOURCE[0] - max_depth - 2, SOURCE[0] + max_depth + 3):
        data.add((i, max_depth + 2))
    while True:
        sand_pos = simulate(SOURCE, data, max_depth + 2)
        if sand_pos:
            sand += 1
            if sand_pos == SOURCE:
                break
            data.add(sand_pos)
        else:
            break
    return sand

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day14.txt')))
    print ('Part Two:', part2(parse_input('input/day14.txt')))
