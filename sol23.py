CHECKS = {'N': [(-1, 0), (-1, 1), (-1, -1)],
          'S': [(1, 0), (1, 1), (1, -1)],
          'W': [(0, -1), (-1, -1), (1, -1)],
          'E': [(0, 1), (-1, 1), (1, 1)]}
DIRS = set((i, j) for i in [-1, 0, 1] for j in [-1, 0, 1]) - {(0, 0)}

def parse_input(input_path: str) -> set[tuple[int, int]]:
    with open(input_path, 'r') as f:
        rows = f.read().strip().split('\n')
        elves = set()
        for r in range(len(rows)):
            for c in range(len(rows[r])):
                if rows[r][c] == '#':
                    elves.add((r, c))
        return elves

def check_no_adj(pos: tuple[int, int], coords: set[tuple[int, int]], dirs: set[tuple[int, int]]) -> bool:
    for d in dirs:
        if (pos[0] + d[0], pos[1] + d[1]) in coords:
            return False
    return True

# Simulates a round, modifying set of elves and returning whether or not any elves moved
def simulate(elves: set[tuple[int, int]], order: list[str]) -> bool:
    proposed = {}
    moved = False
    for elf in elves:
        # Only propose movement if elf has at least one adjacent elf
        if check_no_adj(elf, elves, DIRS):
            continue
        # Iterate through cardinal directions and store proposed move in dictionary
        for orth in order:
            dirs = CHECKS[orth]
            if check_no_adj(elf, elves, set(dirs)):
                move = (elf[0] + dirs[0][0], elf[1] + dirs[0][1])
                if move in proposed:
                    proposed[move].append(elf)
                else:
                    proposed[move] = [elf]
                break
    # Only move elves without proposed collisions
    for move in proposed:
        if len(proposed[move]) == 1:
            elves.add(move)
            elves.remove(proposed[move][0])
            moved = True
    return moved

def part1(data: set[tuple[int, int]]) -> int:
    ITERS = 10
    order = ['N', 'S', 'W', 'E']
    for i in range(ITERS):
        simulate(data, order)
        order.append(order.pop(0))
    min_r = min(elf[0] for elf in data)
    max_r = max(elf[0] for elf in data)
    min_c = min(elf[1] for elf in data)
    max_c = max(elf[1] for elf in data)
    return (max_r - min_r + 1) * (max_c - min_c + 1) - len(data)

def part2(data: set[tuple[int, int]]) -> int:
    rounds = 1
    order = ['N', 'S', 'W', 'E']
    while simulate(data, order):
        rounds += 1
        order.append(order.pop(0))
    return rounds

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day23.txt')))
    print ('Part Two:', part2(parse_input('input/day23.txt')))
