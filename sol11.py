import re

class Monkey:
    def __init__(self, id: int, items: list[int], op: str, test: int, on_true: int, on_false: int):
        self.id = id
        self.items = items
        self.op = op
        self.test = test
        self.on_true = on_true
        self.on_false = on_false
        self.inspections = 0

def parse_input(input_path: str) -> list[Monkey]:
    with open(input_path, 'r') as f:
        monkeys = f.read().split('\n\n')
        monkey_list = []
        for m in monkeys:
            m = m.split('\n')
            id = int(re.search(r'\d+', m[0]).group())
            items = [int(i) for i in re.findall(r'\d+', m[1])]
            op = m[2].split(' = ')[1]
            test = int(re.search(r'\d+', m[3]).group())
            on_true = int(re.search(r'\d+', m[4]).group())
            on_false = int(re.search(r'\d+', m[5]).group())
            monkey_list.append(Monkey(id, items, op, test, on_true, on_false))
        return monkey_list

def part1(data: list[Monkey]) -> int:
    NUM_ROUNDS = 20
    
    for r in range(NUM_ROUNDS):
        for m in data:
            num_items = len(m.items)
            for i in range(num_items):
                item = m.items.pop(0)
                item = eval(m.op.replace('old', str(item))) // 3
                if item % m.test == 0:
                    data[m.on_true].items.append(item)
                else:
                    data[m.on_false].items.append(item)
            m.inspections += num_items

    insp = sorted([m.inspections for m in data], reverse = True)
    return insp[0] * insp[1]

def part2(data: list[Monkey]) -> int:
    NUM_ROUNDS = 10000
    mod = 1 # Divisibility doesn't change when working in Z[LCM of all mods]
    for m in data: # For ease of programming simplifies to product of all mods
        mod *= m.test

    for r in range(NUM_ROUNDS):
        for m in data:
            num_items = len(m.items)
            for i in range(num_items):
                item = m.items.pop(0)
                item = eval(m.op.replace('old', str(item))) % mod
                if item % m.test == 0:
                    data[m.on_true].items.append(item)
                else:
                    data[m.on_false].items.append(item)
            m.inspections += num_items

    insp = sorted([m.inspections for m in data], reverse = True)
    return insp[0] * insp[1]

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day11.txt')))
    print ('Part Two:', part2(parse_input('input/day11.txt')))
