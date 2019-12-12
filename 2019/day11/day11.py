from typing import List, Dict
import time

DEBUG = False

class Robot:
    def __init__(self, name: str, memory: List[int] = []):
        self.name = name
        self.memory = memory + [0] * 1000
        self.counter = 0
        self.relative_base = 0
        self.output = None
        self.halt = False
        self.pause = False
        self.location = (0,0)
        self.direction = 0
        self.output_color = False
        self.painted = {(0,0): 1}

    def run(self):
        while not (self.halt or self.pause):
            instruction = self.decode()
            if instruction['opc'] == 99:
                self.halt = True
                continue
            self.execute(instruction)
        return self.output

    def writeInput(self, input: int):
        self.memory[self.memory[self.counter-1]] = input
        # print(self.name,"received", input, "writing to location", self.memory[self.counter-1])
        self.pause = False
        self.run()

    def decodeParameter(self, offset: int = 0, parameter: int = 1, literal: bool = False) -> int:
        if not literal:
            if parameter == 0: # position mode
                return self.memory[self.memory[self.counter + offset]]
            elif parameter == 1: # direct mode
                return self.memory[self.counter + offset]
            elif parameter == 2: # offset mode
                value = self.memory[self.counter + offset]
                return self.memory[self.relative_base + value]
        else:
            if parameter == 0 or parameter == 1:
                return self.memory[self.counter + offset]
            elif parameter == 2:
                return self.relative_base + self.memory[self.counter + offset]

    def decode(self) -> Dict[str, int]:
        if DEBUG:
            print("Counter:", self.counter)
            print("Memory:", self.memory[self.counter:self.counter+4])
        instruction = {}
        codelist = list(str(self.memory[self.counter]))
        instruction["opc"] = int(''.join(codelist[-2:]))
        for _ in range(5-len(codelist)):
            codelist.insert(0, '0')
        if DEBUG:
            print("Codelist:",codelist)
            print("Rel base:", self.relative_base)
        if instruction["opc"] in [1, 2, 7, 8]:
            instruction["op1"] = self.decodeParameter(1, int(codelist[2]))
            instruction["op2"] = self.decodeParameter(2, int(codelist[1]))
            instruction["acc"] = self.decodeParameter(3, int(codelist[0]), True)
            self.counter += 4
            return instruction
        elif instruction["opc"] in [3, 4, 9]:
            instruction["acc"] = self.decodeParameter(1, int(codelist[2]), True if instruction["opc"] == 3 else False)
            self.counter += 2
            return instruction
        elif instruction["opc"] in [5, 6]:
            instruction["op1"] = self.decodeParameter(1, int(codelist[2]))
            instruction["acc"] = self.decodeParameter(2, int(codelist[1]))
            self.counter += 3
            return instruction
        else: # instruction["opc"] == 99:
            return instruction

    def move(self):
        if self.direction == 0:
            self.location = (self.location[0], self.location[1]+1)
        elif self.direction == 90:
            self.location = (self.location[0]+1, self.location[1])
        elif self.direction == 180:
            self.location = (self.location[0], self.location[1]-1)
        elif self.direction == 270:
            self.location = (self.location[0]-1, self.location[1])

    def execute(self, instruction) -> None:
        if DEBUG:
            print("Instruction: ", instruction)
        if instruction["opc"] == 1:
            self.memory[instruction["acc"]] = instruction["op1"] + instruction["op2"]
        elif instruction["opc"] == 2:
            self.memory[instruction["acc"]] = instruction["op1"] * instruction["op2"]
        elif instruction["opc"] == 3:
            # self.memory[instruction["acc"]] = int(input("Give input: "))
            if self.location in self.painted.keys():
                self.memory[instruction["acc"]] = self.painted[self.location]
            else:
                self.memory[instruction["acc"]] = 0
            # print(self.name,"requesting input")
            # self.pause = True
        elif instruction["opc"] == 4:
            #print("Diagnostic code:", self.memory[instruction["acc"]])
            self.output = instruction["acc"]
            print(self.name, "outputs", self.output)
            if self.output_color:
                direction = 90 if instruction["acc"] == 1 else -90
                self.direction = (self.direction + direction) % 360
                self.move()
            else:
                self.painted[self.location] = instruction["acc"]
            self.output_color = not self.output_color
        elif instruction["opc"] == 5:
            if instruction["op1"] > 0:
                self.counter = instruction["acc"]
        elif instruction["opc"] == 6:
            if instruction["op1"] == 0:
                self.counter = instruction["acc"]
        elif instruction["opc"] == 7:
            if instruction["op1"] < instruction["op2"]:
                self.memory[instruction["acc"]] = 1
            else:
                self.memory[instruction["acc"]] = 0
        elif instruction["opc"] == 8:
            if instruction["op1"] == instruction["op2"]:
                self.memory[instruction["acc"]] = 1
            else:
                self.memory[instruction["acc"]] = 0
        elif instruction["opc"] == 9:
            self.relative_base += instruction["acc"]
        else:
            print("Unknown opcode", instruction, "counter", self.counter)
            input("Pause")


print('----- Program start ------')
start = time.time()
output_values = []
with open("input.txt") as file:
    program = [int(d) for d in file.readline().strip().split(",")]
    # Part 1
    painter = Robot("EHPR", program)
    painter.run()
    print(len(painter.painted.keys()))

    import matplotlib.pyplot as plt
    xdots, ydots = [], []
    for key in painter.painted.keys():
        if painter.painted[key] == 1:
            xdots.append(key[0])
            ydots.append(key[1])
    plt.scatter(xdots, ydots)
    plt.axis([0, 40, -6, 34])
    plt.show()

print('------ completed in %s seconds -------' % str(time.time() - start))