def parse_input(input_path: str) -> list[list[str]]:
    with open(input_path, 'r') as f:
        return [l.replace('$ ', '').split() for l in f.readlines()]

def generate_dirs(commands: list[list[str]]) -> dict[tuple[str], int]:
    dirs = {}
    path = ()
    for cmd in commands:
        # Change directories
        if cmd[0] == 'cd':
            if cmd[1] == '..':
                path = path[:-1]
            else:
                path = path + (cmd[1],)
                dirs.setdefault(path, 0)
        # List directory contents, nothing to do
        elif cmd[0] == 'ls':
            continue
        # Directory exists
        elif cmd[0] == 'dir':
            dirs.setdefault(path + (cmd[1],), 0)
        # File exists
        else:
            size = int(cmd[0])
            # Add file size to all directories containing it
            for depth in range(len(path), 0, -1):
                dirs[path[:depth]] += size
    return dirs

def part1(data: list[list[str]]) -> int:
    total = 0
    dirs = generate_dirs(data)
    for path in dirs:
        if dirs[path] <= 100000:
            total += dirs[path]
    return total

def part2(data: list[list[str]]) -> int:
    dirs = generate_dirs(data)
    TOTAL_SPACE = 70000000
    UPDATE_SIZE = 30000000
    USED_SPACE = dirs[('/',)]
    MIN_DELETE = UPDATE_SIZE - (TOTAL_SPACE - USED_SPACE)

    min_dir = USED_SPACE
    for path in dirs:
        if dirs[path] >= MIN_DELETE and dirs[path] < min_dir:
            min_dir = dirs[path]
    return min_dir
    

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day07.txt')))
    print ('Part Two:', part2(parse_input('input/day07.txt')))
