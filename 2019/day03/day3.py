from typing import Tuple, List

def manhattan_distance(point: Tuple[int, int]) -> int:
    return abs(point[0]) + abs(point[1])

def parse_list(instructions: List[str]) -> List[Tuple[int, int]]:
    pos = (0, 0)
    result = [pos]
    for instruction in instructions:
        result = result + make_step(instruction, pos)
        pos = result[-1]
    return result

def make_step(instruction: str, position: Tuple[int, int]) -> List[Tuple[int, int]]:
    direction = instruction[0]
    step = int(instruction[1:])
    xpos, ypos = position
    if direction == "U":
        result = []
        for i in range(step):
            result.append((xpos,ypos+1+i))
        return result
    elif direction == "D":
        result = []
        for i in range(step):
            result.append((xpos,ypos-1-i))
        return result
    elif direction == "R":
        result = []
        for i in range(step):
            result.append((xpos+1+i,ypos))
        return result
    elif direction == "L":
        result = []
        for i in range(step):
            result.append((xpos-1-i,ypos))
        return result
    else:
        return [position]

def find_overlap(list1: List[Tuple[int, int]], list2: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    result = []
    for item in list1:
        if item in list2:
            result.append(item)
    return result


with open("input.txt") as file:
    line1 = file.readline()
    line1 = line1.split(',')
    line2 = file.readline()
    line2 = line2.split(',')

list1 = parse_list(line1)
list2 = parse_list(line2)
overlap = find_overlap(list1, list2)
overlap.remove((0,0))
# distances = []
# for i in overlap:
#     distances.append(manhattan_distance(i))
# print(min(distances))
min = 10000000
min_overlap = (0,0)
for o in overlap:
    steps1 = list1.index(o)
    steps2 = list2.index(o)
    if steps1 + steps2 < min:
        min = steps1 + steps2
        min_overlap = o
print(min)
