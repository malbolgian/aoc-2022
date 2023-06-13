from typing import Callable

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class Face:
    def __init__(self, id: int, topleft: tuple[int, int]):
        self.id = id
        self.topleft = topleft
        self.adj = {}

    def add_adj(self, current_dir: tuple[int, int], out_dir: tuple[int, int], trans_func: Callable[[tuple[int, int]], tuple[int, int]]) -> None:
        self.adj[current_dir] = (out_dir, trans_func)

def initialize_cube() -> list[Face]:
    f0, f1, f2, f3, f4, f5 = Face(0, (0, 50)), Face(1, (0, 100)), Face(2, (50, 50)), Face(3, (100, 0)), Face(4, (100, 50)), Face(5, (150, 0))
    
    f0.add_adj(DIRS[2], DIRS[0], lambda t: (149 - t[0], 0))
    f0.add_adj(DIRS[3], DIRS[0], lambda t: (100 + t[1], 0))
    
    f1.add_adj(DIRS[0], DIRS[2], lambda t: (149 - t[0], 99))
    f1.add_adj(DIRS[1], DIRS[2], lambda t: (t[1] - 50, 99))
    f1.add_adj(DIRS[3], DIRS[3], lambda t: (199, t[1] - 100))
    
    f2.add_adj(DIRS[0], DIRS[3], lambda t: (49, t[0] + 50))
    f2.add_adj(DIRS[2], DIRS[1], lambda t: (100, t[0] - 50))
    
    f3.add_adj(DIRS[2], DIRS[0], lambda t: (149 - t[0], 50))
    f3.add_adj(DIRS[3], DIRS[0], lambda t: (50 + t[1], 50))

    f4.add_adj(DIRS[0], DIRS[2], lambda t: (149 - t[0], 149))
    f4.add_adj(DIRS[1], DIRS[2], lambda t: (100 + t[1], 49))

    f5.add_adj(DIRS[0], DIRS[3], lambda t: (149, t[0] - 100))
    f5.add_adj(DIRS[1], DIRS[1], lambda t: (0, t[1] + 100))
    f5.add_adj(DIRS[2], DIRS[1], lambda t: (0, t[0] - 100))
    
    return [f0, f1, f2, f3, f4, f5]

def point2face(point: tuple[int, int], cube: list[Face]) -> int:
    for f in cube:
        if (f.topleft[0] <= point[0] < f.topleft[0] + 50) and (f.topleft[1] <= point[1] < f.topleft[1] + 50):
            return f.id

def parse_input(input_path: str) -> tuple[dict[tuple[int, int], str], list[str]]:
    with open(input_path, 'r') as f:
        board_string, move_string = f.read().split('\n\n')
        board_lines = board_string.split('\n')
        board = {}
        for r in range(len(board_lines)):
            for c in range(len(board_lines[r])):
                if board_lines[r][c] in '.#':
                    board[(r, c)] = board_lines[r][c]
        move_string = move_string.strip().replace('L', ' L ').replace('R', ' R ')
        moves = move_string.split(' ')
        return board, moves

def part1(data: tuple[dict[tuple[int, int], str], list[str]]) -> int:
    board, moves = data
    MAX_ROW = max(point[0] for point in board)
    MAX_COL = max(point[1] for point in board)
    pos = (0, MAX_COL)
    d = 0
    for point in board:
        if point[0] == 0 and board[point] == '.' and point[1] < pos[1]:
            pos = point

    for move in moves:
        if move == 'L':
            d = (d - 1) % 4
        elif move == 'R':
            d = (d + 1) % 4
        else:
            for i in range(int(move)):
                new_row = (pos[0] + DIRS[d][0]) % (MAX_ROW + 1)
                new_col = (pos[1] + DIRS[d][1]) % (MAX_COL + 1)
                while (new_row, new_col) not in board:
                    new_row = (new_row + DIRS[d][0]) % (MAX_ROW + 1)
                    new_col = (new_col + DIRS[d][1]) % (MAX_COL + 1)
                if board[(new_row, new_col)] == '#':
                    break
                pos = (new_row, new_col)
    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + d

def part2(data: tuple[dict[tuple[int, int], str], list[str]]) -> int:
    # NOTE: Cube initialization is currently specific to the input and will not work on all test cases.
    CUBE = initialize_cube()
    board, moves = data
    MAX_ROW = max(point[0] for point in board)
    MAX_COL = max(point[1] for point in board)
    pos = (0, MAX_COL)
    face = 0
    d = 0
    for point in board:
        if point[0] == 0 and board[point] == '.' and point[1] < pos[1]:
            pos = point

    for move in moves:
        if move == 'L':
            d = (d - 1) % 4
        elif move == 'R':
            d = (d + 1) % 4
        else:
            for i in range(int(move)):
                new_row = pos[0] + DIRS[d][0]
                new_col = pos[1] + DIRS[d][1]
                new_dir = DIRS[d]
                if (new_row, new_col) not in board:
                    new_dir, trans_func = CUBE[face].adj[new_dir]
                    new_row, new_col = trans_func((new_row, new_col))
                if board[(new_row, new_col)] == '#':
                    break
                pos = (new_row, new_col)
                face = point2face(pos, CUBE)
                d = DIRS.index(new_dir)
    return 1000 * (pos[0] + 1) + 4 * (pos[1] + 1) + d

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day22.txt')))
    print ('Part Two:', part2(parse_input('input/day22.txt')))
