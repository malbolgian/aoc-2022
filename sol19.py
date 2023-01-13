import re

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE = 3
MATERIALS = 4

class Blueprint:
    def __init__(self, id: int, costs: dict[int, tuple[int, int, int]]):
        self.id = id
        self.costs = costs
        self.limits = list(map(max, zip(*[costs[robot] for robot in range(MATERIALS)])))
        self.limits[GEODE] = float('inf')

    def buildable(self, robots: list[int], resources: list[int], time_left: int) -> list[int]:
        can_build = []
        for material in self.costs:
            # If you have enough resources to build the robot
            if all(resources[i] >= self.costs[material][i] for i in range(len(resources))):
                # Optimization: Stop building robots once we have enough predicted material to build for the remaining rounds
                if resources[material] + robots[material] * time_left < self.limits[material] * time_left:
                    can_build.append(material)
        return can_build

    def build_robot(self, robot: int, resources: list[int]) -> list[int]:
        return [resources[i] - self.costs[robot][i] for i in range(MATERIALS)]

def parse_input(input_path: str) -> list[Blueprint]:
    with open(input_path, 'r') as f:
        blueprints = []
        lines = f.read().strip().split('\n')
        for line in lines:
            line = line.replace(':', '.').split('. ')
            costs = {}
            id = int(line[0].split()[1])
            costs[0] = (int(line[1].split()[4]), 0, 0, 0)
            costs[1] = (int(line[2].split()[4]), 0, 0, 0)
            costs[2] = (int(line[3].split()[4]), int(line[3].split()[7]), 0, 0)
            costs[3] = (int(line[4].split()[4]), 0, int(line[4].split()[7]), 0)
            blueprints.append(Blueprint(id, costs))
        return blueprints

def part1(data: list[Blueprint]) -> int:
    quality = 0
    MAX_TIME = 24
    for bp in data:
        max_geodes = 0
        stack = [([1, 0, 0, 0], [0, 0, 0, 0], 1, [])]

        while len(stack) > 0:
            robots, resources, time, skipped = stack.pop()
            time_left = MAX_TIME - time
            to_build = bp.buildable(robots, resources, time_left)
            resources = [robots[i] + resources[i] for i in range(MATERIALS)]
            if time == MAX_TIME:
                max_geodes = max(max_geodes, resources[GEODE])
                continue
            # Optimization: If the potential maximum geodes is less than the current maximum, terminate branch
            potential = resources[GEODE] + \
                        time_left * robots[GEODE] + \
                        time_left * (time_left + 1) // 2
            if potential <= max_geodes:
                continue
            # Optimization: If we did nothing instead of building a robot the previous timestep, do not build the robot this timestep
            stack.append((robots, resources, time + 1, to_build))
            for robot in to_build:
                if robot in skipped:
                    continue
                new_robots = robots.copy()
                new_robots[robot] += 1
                new_resources = bp.build_robot(robot, resources)
                stack.append((new_robots, new_resources, time + 1, []))

        quality += (bp.id * max_geodes)
    return quality

def part2(data: list[Blueprint]) -> int:
    product = 1
    MAX_TIME = 32
    for bp in data[:3]:
        max_geodes = 0
        stack = [([1, 0, 0, 0], [0, 0, 0, 0], 1, [])]

        while len(stack) > 0:
            robots, resources, time, skipped = stack.pop()
            time_left = MAX_TIME - time
            to_build = bp.buildable(robots, resources, time_left)
            resources = [robots[i] + resources[i] for i in range(MATERIALS)]
            if time == MAX_TIME:
                max_geodes = max(max_geodes, resources[GEODE])
                continue

            potential = resources[GEODE] + \
                        time_left * robots[GEODE] + \
                        time_left * (time_left + 1) // 2
            if potential <= max_geodes:
                continue

            stack.append((robots, resources, time + 1, to_build))
            for robot in to_build:
                if robot in skipped:
                    continue
                new_robots = robots.copy()
                new_robots[robot] += 1
                new_resources = bp.build_robot(robot, resources)
                stack.append((new_robots, new_resources, time + 1, []))

        product *= max_geodes
    return product

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day19.txt')))
    print ('Part Two:', part2(parse_input('input/day19.txt')))
