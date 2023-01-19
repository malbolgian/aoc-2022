from typing import Callable, Optional

OPS = {'+': lambda l, r: l + r,
       '-': lambda l, r: l - r,
       '*': lambda l, r: l * r,
       '/': lambda l, r: l // r}

INV_RIGHT = {'+': lambda l, out: out - l,
             '-': lambda l, out: l - out,
             '*': lambda l, out: out // l,
             '/': lambda l, out: l // out}

INV_LEFT = {'+': lambda r, out: out - r,
            '-': lambda r, out: out + r,
            '*': lambda r, out: out // r,
            '/': lambda r, out: out * r}

class Monkey:
    def __init__(self, value: int = None, left: str = None, right: str = None, func: str = None):
        self.value = value
        self.left = left
        self.right = right
        self.func = func

def parse_input(input_path: str) -> dict[str, Monkey]:
    with open(input_path, 'r') as f:
        lines = f.read().strip().split('\n')
        monkeys = {}
        for m in lines:
            id, expr = m.split(': ')
            if expr.isdigit():
                if id in monkeys:
                    monkeys[id].value = int(expr)
                else:
                    monkeys[id] = Monkey(value = int(expr))
            else:
                left_id, op, right_id = expr.split(' ')
                for child in [left_id, right_id]:
                    if child not in monkeys:
                        monkeys[child] = Monkey()
                if id in monkeys:
                    monkeys[id].left = left_id
                    monkeys[id].right = right_id
                    monkeys[id].func = op
                else:
                    monkeys[id] = Monkey(left = left_id, right = right_id, func = op)
        return monkeys

# Recursively calculate the values of the monkeys
def calculate(id: str, monkeys: dict[str, Monkey]) -> int:
    monkey = monkeys[id]
    # If monkey is not a leaf node, calculate children first then evaluate
    if monkey.func:
        left_val = calculate(monkey.left, monkeys)
        right_val = calculate(monkey.right, monkeys)
        monkey.value = OPS[monkey.func](left_val, right_val)
    return monkey.value

# Find the path from given start to end nodes, returns list of directions to take
def find_path(start: Optional[str], end: str, monkeys: dict[str, Monkey]) -> Optional[list[str]]:
    if start is None:
        return None
    if start == end:
        return []
    path = find_path(monkeys[start].left, end, monkeys)
    if path is not None:
        return ['left'] + path
    path = find_path(monkeys[start].right, end, monkeys)
    if path is not None:
        return ['right'] + path

def part1(data: dict[str, Monkey]) -> int:
    return calculate('root', data)

def part2(data: dict[str, Monkey]) -> int:
    path = find_path('root', 'humn', data)
    current = 'root'
    # For each monkey along the path: calculate the value of the child not on the path, then store the passing value of the child on the path in goal
    for direction in path:
        monkey = data[current]
        if direction == 'left':
            right_value = calculate(monkey.right, data)
            goal = right_value if current == 'root' else INV_LEFT[monkey.func](right_value, goal)
            current = monkey.left
        else:
            left_value = calculate(monkey.left, data)
            goal = left_value if current == 'root' else INV_RIGHT[monkey.func](left_value, goal)
            current = data[current].right
    return goal    

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day21.txt')))
    print ('Part Two:', part2(parse_input('input/day21.txt')))
