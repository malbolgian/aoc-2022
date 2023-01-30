from math import lcm

DIRS = {'^': (-1, 0),
        '>': (0, 1),
        'v': (1, 0),
        '<': (0, -1)}

def parse_input(input_path: str) -> tuple[int, int, dict[str, set[tuple[int, int]]]]:
    with open(input_path, 'r') as f:
        x = [line[1:-1] for line in f.read().strip().split('\n')[1:-1]]
        winds = {}
        for d in DIRS:
            winds[d] = set()
        rows, cols = len(x), len(x[0])
        for row in range(rows):
            for col in range(cols):
                char = x[row][col]
                if char in DIRS:
                    winds[char].add((row, col))    
        return rows, cols, winds

def all_safe(data: tuple[int, int, dict[str, set[tuple[int, int]]]]) -> list[set[tuple[int, int]]]:
    rows, cols, winds = data
    period = lcm(rows, cols)
    all_space = set((i, j) for i in range(rows) for j in range(cols))
    safe = []
    for t in range(period):
        # Determine safe spaces by removing winds from all possible spaces
        all_winds = set()
        for d in DIRS:
            all_winds |= winds[d]
        safe.append(all_space - all_winds)
        # Shift winds by one timestep
        for d in DIRS:
            winds[d] = set(((wind[0] + DIRS[d][0]) % rows, (wind[1] + DIRS[d][1]) % cols) for wind in winds[d])
    return safe

def traverse(start: tuple[int, int], end: tuple[int, int], safe_list: list[set[tuple[int, int]]], start_time: int) -> int:
    period = len(safe_list)
    queue = [(start, start_time)]

    while len(queue) > 0:
        pos, time = queue.pop(0)
        if pos == end:
            return time
        safe_spaces = safe_list[(time + 1) % period] | {end}
        # Move in a direction only if the resulting space is safe during the next timestep
        for d in DIRS:
            test_pos = (pos[0] + DIRS[d][0], pos[1] + DIRS[d][1])
            if test_pos in safe_spaces and (test_pos, time + 1) not in queue:
                queue.append((test_pos, time + 1))
        # Waiting is allowed if the current space is safe during the next timestep, or if it's the starting location
        # Keeping starting location separate from safe spaces prevents moving back into the start after leaving
        if (pos in safe_spaces or pos == start) and (pos, time + 1) not in queue:
            queue.append((pos, time + 1))

def part1(data: tuple[int, int, dict[str, set[tuple[int, int]]]]) -> int:
    rows, cols, winds = data
    START = (-1, 0)
    END = (rows, cols - 1)
    safe_list = all_safe(data)
    return traverse(START, END, safe_list, 0)

def part2(data: tuple[int, int, dict[str, set[tuple[int, int]]]]) -> int:
    rows, cols, winds = data
    START = (-1, 0)
    END = (rows, cols - 1)
    safe_list = all_safe(data)

    check1 = traverse(START, END, safe_list, 0)
    check2 = traverse(END, START, safe_list, check1)
    return traverse(START, END, safe_list, check2)

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day24.txt')))
    print ('Part Two:', part2(parse_input('input/day24.txt')))
