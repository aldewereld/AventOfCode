from typing import List, Dict
import time

DEBUG = False

class Computer:
    def __init__(self, name: str, memory: List[int] = []):
        self.name = name
        self.memory = memory + [0] * 1000
        self.counter = 0
        self.relative_base = 0
        self.output = None
        self.halt = False
        self.pause = False

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

    def execute(self, instruction) -> None:
        if DEBUG:
            print("Instruction: ", instruction)
        if instruction["opc"] == 1:
            self.memory[instruction["acc"]] = instruction["op1"] + instruction["op2"]
        elif instruction["opc"] == 2:
            self.memory[instruction["acc"]] = instruction["op1"] * instruction["op2"]
        elif instruction["opc"] == 3:
            self.memory[instruction["acc"]] = int(input("Give input: "))
            # print(self.name,"requesting input")
            # self.pause = True
        elif instruction["opc"] == 4:
            #print("Diagnostic code:", self.memory[instruction["acc"]])
            self.output = instruction["acc"]
            print(self.name, "outputs", self.output)
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
    # program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    # program = [1102,34915192,34915192,7,4,7,99,0]
    # program = [104,1125899906842624,99]
    # Part 1
    boost = Computer("BOOST", program)
    boost.run()

print('------ completed in %s seconds -------' % str(time.time() - start))