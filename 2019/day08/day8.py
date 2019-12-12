from typing import List, Tuple
from functools import reduce

with open("input.txt") as file:
    line = list(file.readline().strip())

def split_layers(input_message: List[str], width: int = 25, height: int = 6) -> List[List[str]]:
    layers = []
    start = 0
    step = width * height
    end = step
    for i in range(0, len(input_message), step):
        layers.append(input_message[start:end])
        start, end = end, end+step
    return layers

def count(object: int, list: List[int]) -> int:
    if list == []:
        return 0
    else:
        head, *tail = list
        if head == object:
            return 1+count(object, tail)
        else:
            return count(object, tail)


# Part 1
layers = split_layers(line)
counted = list(map(lambda x: count('0', x), layers))
least_zeros = min(counted)
index = counted.index(least_zeros)
ones, twos = count('1', layers[index]), count('2', layers[index])
print(ones * twos)

# Part 2
#layers = split_layers(list("0222112222120000"), 2, 2)

def decode_layers(layer1: List[int], layer2: List[int]) -> List[int]:
    return list(map(decode_pixel, zip(layer1, layer2)))

def decode_pixel(pixel_pair: Tuple[int, int]) -> int:
    if pixel_pair[0] == '2': # if transparent
        return pixel_pair[1] # return lower pixel
    else: # else use upper pixel
        return pixel_pair[0]

image = reduce(decode_layers, layers)

start = 0
end = 25
for _ in range(6):
    print(image[start:end])
    start, end = end, end+25