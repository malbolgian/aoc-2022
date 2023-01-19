from collections import deque

def parse_input(input_path: str) -> list[int]:
    with open(input_path, 'r') as f:
        coords = [int(i) for i in f.read().strip().split('\n')]
        return coords

def mix(coords: deque[tuple[int, int]], rounds: int) -> deque[tuple[int, int]]:
    mixed = coords.copy()
    for i in range(rounds):
        for coord in coords:
            mixed.rotate(-1 * mixed.index(coord))
            mixed.popleft()
            mixed.rotate(-1 * coord[1] % len(mixed))
            mixed.appendleft(coord)
    return mixed

def calculate_coords(coords: deque[tuple[int, int]]) -> int:
    index0 = 0
    while coords[index0][1] != 0:
        index0 += 1
    return sum(coords[(index0 + offset) % len(coords)][1] for offset in [1000, 2000, 3000])

def part1(data: list[int]) -> int:
    # Enumeration with index necessary to handle duplicate numbers
    coords = deque(list(enumerate(data)))
    mixed = mix(coords, 1)
    return calculate_coords(mixed)

def part2(data: list[int]) -> int:
    KEY = 811589153
    data = [KEY * i for i in data]
    coords = deque(list(enumerate(data)))
    mixed = mix(coords, 10)
    return calculate_coords(mixed)

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day20.txt')))
    print ('Part Two:', part2(parse_input('input/day20.txt')))
