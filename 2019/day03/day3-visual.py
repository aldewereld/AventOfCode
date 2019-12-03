import pygame
from typing import List, Tuple

with open("input.txt") as file:
    line1 = file.readline().split(",")
    line2 = file.readline().split(",")

pygame.init()
surface = pygame.display.set_mode((1024,800))
surface.fill((255,255,255))

origin = (212, 400)
stepSize = 0.05

def drawLine(instructions: List[Tuple[int, int]], colour: Tuple[int, int, int]) -> None:
    pos = origin
    for instruction in instructions:
        direction = instruction[0]
        steps = int(instruction[1:])
        if direction == "U":
            newpos = (pos[0], pos[1]+stepSize*steps)
            pygame.draw.line(surface, colour, pos, newpos)
        elif direction == "D":
            newpos = (pos[0], pos[1]-stepSize*steps)
            pygame.draw.line(surface, colour, pos, newpos)
        elif direction == "R":
            newpos = (pos[0]+stepSize*steps, pos[1])
            pygame.draw.line(surface, colour, pos, newpos)
        elif direction == "L":
            newpos = (pos[0]-stepSize*steps, pos[1])
            pygame.draw.line(surface, colour, pos, newpos)
        pos = newpos

drawLine(line1, (255, 0, 0))
drawLine(line2, (0, 0, 255))

pygame.display.flip()
clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    clock.tick(2)
