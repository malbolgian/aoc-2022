import re

class Valve:
    def __init__(self, name: str, flow: int, adj: list[str]):
        self.name = name
        self.flow = flow
        self.adj = adj

def parse_input(input_path: str) -> tuple[list[Valve], dict[str, int]]:
    with open(input_path, 'r') as f:
        valves = []
        index = {}
        i = 0
        lines = f.read().strip().split('\n')
        for line in lines:
            split = line.split(' ')
            valve = split[1]
            flow = int(re.search(r'\d+', line).group())
            adj = []
            if 'valves' in split:
                for ind in range(split.index('valves') + 1, len(split)):
                    adj.append(split[ind][:2])
            else:
                adj.append(split[-1])
            valves.append(Valve(valve, flow, adj))
            index[valve] = i
            i += 1
        return valves, index

def calculate_dist(valves: list[Valve], index: dict[str, int]) -> tuple[dict[tuple[str, str], int], dict[str, int]]:
    dist = [[float('inf') for j in range(len(valves))] for i in range(len(valves))]
    for i in range(len(valves)):
        dist[i][i] = 0
    for v in valves:
        for tunnel in v.adj:
            dist[index[v.name]][index[tunnel]] = 1
    for k in range(len(valves)):
        for i in range(len(valves)):
            for j in range(len(valves)):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    # Only keep information about starting valve and valves with positive flow rate
    relevant_flow = {}
    for v in valves:
        if v.name == 'AA' or v.flow > 0:
            relevant_flow[v.name] = v.flow
    relevant_dist = {}
    for valve1 in relevant_flow:
        for valve2 in relevant_flow:
            relevant_dist[(valve1, valve2)] = dist[index[valve1]][index[valve2]]
    return relevant_dist, relevant_flow

def part1(data: tuple[list[Valve], dict[str, int]]) -> int:
    valves, index = data
    dist, flows = calculate_dist(valves, index)
    relevant = list(flows.keys())
    START = 'AA'
    MAX_TIME = 30
    relevant.remove(START)
    queue = [(START, 0, 0, 0, relevant)]
    max_flow = 0

    while len(queue) > 0:
        valve, time, current_flow, total_flow, closed_valves = queue.pop()
        if len(closed_valves) == 0: # If all relevant valves are open, calculate total
            flow = (MAX_TIME - time) * current_flow + total_flow
            if flow > max_flow:
                max_flow = flow
            continue
        for new_valve in closed_valves:
            elapsed_time = dist[(valve, new_valve)] + 1 # Travel to the next valve and open it
            if (time + elapsed_time) >= MAX_TIME: # If opening the next valve takes too long, calculate total
                flow = (MAX_TIME - time) * current_flow + total_flow
                if flow > max_flow:
                    max_flow = flow
                continue
            new_total_flow = total_flow + elapsed_time * current_flow
            new_time = time + elapsed_time
            new_current_flow = current_flow + flows[new_valve]
            new_closed_valves = closed_valves.copy()
            new_closed_valves.remove(new_valve)
            queue.append((new_valve, new_time, new_current_flow, new_total_flow, new_closed_valves))
    return max_flow

def part2(data: tuple[list[Valve], dict[str, int]]) -> int:
    valves, index = data
    dist, flows = calculate_dist(valves, index)
    relevant = list(flows.keys())
    START = 'AA'
    MAX_TIME = 26
    relevant.remove(START)
    queue = [(START, 0, 0, 0, relevant, set())]
    max_flows = {} # Stores maximum flows for every set of visited nodes

    while len(queue) > 0:
        valve, time, current_flow, total_flow, closed_valves, open_valves = queue.pop()
        # Assume no other valves are opened and store the total flow if greater than the maximum so far
        flow = (MAX_TIME - time) * current_flow + total_flow
        key = frozenset(open_valves)
        if flow > max_flows.setdefault(key, 0):
            max_flows[key] = flow
        # Expand the set of open valves as long as it can open another valve in time
        for new_valve in closed_valves:
            elapsed_time = dist[(valve, new_valve)] + 1
            if (time + elapsed_time) >= MAX_TIME:
                continue
            new_total_flow = total_flow + elapsed_time * current_flow
            new_time = time + elapsed_time
            new_current_flow = current_flow + flows[new_valve]
            new_closed_valves = closed_valves.copy()
            new_closed_valves.remove(new_valve)
            new_open_valves = open_valves.copy()
            new_open_valves.add(new_valve)
            queue.append((new_valve, new_time, new_current_flow, new_total_flow, new_closed_valves, new_open_valves))
    # Calculate the largest possible sum of opening two mutually-exclusive sets of valves
    max_flow = 0
    for open_valves in max_flows:
        for open_valves_2 in max_flows:
            if len(open_valves.intersection(open_valves_2)) == 0:
                flow = max_flows[open_valves] + max_flows[open_valves_2]
                if flow > max_flow:
                    max_flow = flow
    return max_flow

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day16.txt')))
    print ('Part Two:', part2(parse_input('input/day16.txt')))
