import re
from typing import Optional

def parse_input(input_path: str) -> tuple[list[tuple[int, int, int]], list[tuple[int, int]]]:
    with open(input_path, 'r') as f:
        lines = f.read().strip().split('\n')
        sensors = []
        beacons = []
        for line in lines:
            nums = [int(i) for i in re.findall(r'-?\d+', line)]
            dist = abs(nums[2] - nums[0]) + abs(nums[3] - nums[1])
            sensors.append((nums[0], nums[1], dist))
            beacons.append((nums[2], nums[3]))
        beacons = list(set(beacons))
        return sensors, beacons

def beaconless(row: int, sensors: list[tuple[int, int, int]], min_coord: Optional[int], max_coord: Optional[int]) -> list[list[int]]:
    intervals = []
    for scol, srow, dist in sensors:
        if abs(row - srow) > dist:
            continue
        horizontal = dist - abs(row - srow)
        interval = [scol - horizontal, scol + horizontal]
        if min_coord != None and max_coord != None:
            if interval[1] < min_coord or interval[0] > max_coord:
                continue
            interval[0] = max(interval[0], min_coord)
            interval[1] = min(interval[1], max_coord)
        intervals.append(interval)
    # Consolidate potentially intersecting intervals into mutually-exclusive intervals
    intervals.sort()
    positions = []
    for interval in intervals:
        if len(positions) == 0 or interval[0] > positions[-1][1]:
            positions.append(interval)
        else:
            positions[-1][1] = max(positions[-1][1], interval[1])
    return positions

def part1(data: tuple[list[tuple[int, int, int]], list[tuple[int, int]]]) -> int:
    ROW = 2000000
    sensors, beacons = data
    beacons_in_row = list(filter(lambda tup: tup[1] == ROW, beacons))
    positions = beaconless(ROW, sensors, None, None)
    total = 0
    for interval in positions:
        total += (interval[1] - interval[0] + 1)
        for beacon in beacons_in_row:
            if interval[0] <= beacon[0] <= interval[1]:
                total -= 1
    return total

def part2(data: tuple[list[tuple[int, int, int]], list[tuple[int, int]]]) -> int:
    MIN_COORD = 0
    MAX_COORD = 4000000
    sensors = data[0]
    for row in range(MAX_COORD):
        total = 0
        positions = beaconless(row, sensors, MIN_COORD, MAX_COORD)
        # Use the fact that for all full rows, positions = [[MIN_COORD, MAX_COORD]]
        interval = positions[0]
        if interval[0] != MIN_COORD:
            return row
        if interval[1] != MAX_COORD:
            return MAX_COORD * (interval[1] + 1) + row

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day15.txt')))
    print ('Part Two:', part2(parse_input('input/day15.txt')))
