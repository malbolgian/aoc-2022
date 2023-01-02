class Rock:
    def __init__(self, shape: int, height: int):
        if shape == 0:
            self.coords = {(2, height + 4),
                           (3, height + 4),
                           (4, height + 4),
                           (5, height + 4)}
        elif shape == 1:
            self.coords = {(3, height + 4),
                           (2, height + 5),
                           (3, height + 5),
                           (4, height + 5),
                           (3, height + 6)}
        elif shape == 2:
            self.coords = {(2, height + 4),
                           (3, height + 4),
                           (4, height + 4),
                           (4, height + 5),
                           (4, height + 6)}
        elif shape == 3:
            self.coords = {(2, height + 4),
                           (2, height + 5),
                           (2, height + 6),
                           (2, height + 7)}
        elif shape == 4:
            self.coords = {(2, height + 4),
                           (3, height + 4),
                           (2, height + 5),
                           (3, height + 5)}

    def move_left(self, stops: set[tuple[int, int]]) -> None:
        for coord in self.coords:
            if coord[0] == 0 or (coord[0] - 1, coord[1]) in stops:
                return
        self.coords = set((coord[0] - 1, coord[1]) for coord in self.coords)

    def move_right(self, stops: set[tuple[int, int]]) -> None:
        for coord in self.coords:
            if coord[0] == 6 or (coord[0] + 1, coord[1]) in stops:
                return
        self.coords = set((coord[0] + 1, coord[1]) for coord in self.coords)

    def move_down(self, stops: set[tuple[int, int]]) -> bool:
        for coord in self.coords:
            if (coord[0], coord[1] - 1) in stops:
                return False
        self.coords = set((coord[0], coord[1] - 1) for coord in self.coords)
        return True

    def get_height(self) -> int:
        return max(coord[1] for coord in self.coords)

    def get_left_edge(self) -> int:
        return min(coord[0] for coord in self.coords)

def parse_input(input_path: str) -> str:
    with open(input_path, 'r') as f:
        return f.read().strip()

def part1(data: str) -> int:
    NUM_ROCKS = 2022
    wind_index = 0
    total_height = 0
    stops = {(i, 0) for i in range(7)} # Initialized with representation of floor
    for rock_index in range(NUM_ROCKS):
        rock = Rock(rock_index % 5, total_height)
        falling = True
        while falling:
            if data[wind_index] == '<':
                rock.move_left(stops)
            else:
                rock.move_right(stops)
            falling = rock.move_down(stops)
            wind_index += 1
            if wind_index == len(data):
                wind_index = 0
        stops.update(rock.coords)
        total_height = max(total_height, rock.get_height())
        del rock
    return total_height

def part2(data: str) -> int:
    max_iter = int(1e12)
    wind_index = 0
    rock_index = 0
    total_height = 0
    horizontals = {} # Dictionary containing positions and L/R indices of horizontal pieces
    searching = True # boolean value containing whether or not we're looking for a cycle, False after cycle is found
    first_pass = True # boolean value containing whether or not we're in the first pass of L/R moves, False after completing a full set
    stops = {(i, 0) for i in range(7)}
    while rock_index < max_iter:
        rock = Rock(rock_index % 5, total_height)        
        falling = True
        while falling:
            if data[wind_index] == '<':
                rock.move_left(stops)
            else:
                rock.move_right(stops)
            falling = rock.move_down(stops)
            wind_index += 1
            if wind_index == len(data):
                first_pass = False
                wind_index = 0
        stops.update(rock.coords)
        total_height = max(total_height, rock.get_height())
        # Criteria for checking a cycle beginning with a horizontal piece:
        #   Went through list of L/R moves at least once
        #   Horizontal piece is at the top of the rock pile
        #   Horizontal piece isn't all the way to either end (so + piece has to stack on top)
        # Likely not complete but good enough (?)
        if (not first_pass) and searching and (rock_index % 5 == 0) and (rock.get_left_edge() not in (0, 3)) and (rock.get_height() == total_height):
            horizontal_key = (rock.get_left_edge(), wind_index)
            if horizontal_key in horizontals:
                piece_diff = rock_index - horizontals[horizontal_key][0]
                height_diff = total_height - horizontals[horizontal_key][1]
                skip_cycles = (max_iter - rock_index - 1) // piece_diff
                max_iter -= (skip_cycles * piece_diff) # Decrease the loop bound by cycles skipped
                searching = False
            else:
                horizontals[horizontal_key] = (rock_index, total_height)
        del rock
        rock_index += 1
    return total_height + (skip_cycles * height_diff) # Add in the height from skipped cycles

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day17.txt')))
    print ('Part Two:', part2(parse_input('input/day17.txt')))
