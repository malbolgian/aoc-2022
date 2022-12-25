def parse_input(input_path: str) -> list[str]:
    with open(input_path, 'r') as f:
        return f.read().strip().split('\n')

def part1(data: list[str]) -> int:
    xreg = 1
    cycle = 0
    poll = 20
    signal = 0
    
    for line in data:
        if line[:4] == 'noop':
            cycle += 1
            toadd = 0
        else:
            cycle += 2
            toadd = int(line[5:])
        if cycle >= poll:
            signal += poll * xreg
            poll += 40
        xreg += toadd
    return signal

def draw(cycle: int, xreg: int, size: int) -> str:
    if abs(cycle % size - xreg) <= 1:
        return '#'
    return '.'

def part2(data: list[str]) -> list[str]:
    xreg = 1
    cycle = 0
    pixels = ''
    ROW_SIZE = 40
    
    for line in data:
        if line[:4] == 'noop':
            pixels += draw(cycle, xreg, ROW_SIZE)
            cycle += 1
            toadd = 0
        else:
            pixels += draw(cycle, xreg, ROW_SIZE)
            pixels += draw(cycle + 1, xreg, ROW_SIZE)
            cycle += 2
            toadd = int(line[5:])
        xreg += toadd
    return [pixels[i:i+ROW_SIZE] for i in range(0, len(pixels), ROW_SIZE)]

if __name__ == '__main__':
    print ('Part One:', part1(parse_input('input/day10.txt')))
    print ('Part Two:')
    out = part2(parse_input('input/day10.txt'))
    for line in out:
        print (line)
