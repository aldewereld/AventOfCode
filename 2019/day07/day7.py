from typing import List, Dict, TypeVar
import time
from itertools import permutations
from copy import deepcopy

AmplifierCircuit = TypeVar("AmplifierCircuit")

class Computer:
    def __init__(self, name: str, memory: List[int] = [], controller: AmplifierCircuit = None):
        self.name = name
        self.memory = memory
        self.controller = controller
        self.counter = 0
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

    def decode(self) -> Dict[str, int]:
        # print("Counter:", self.counter)
        # print("Memory:", self.memory[self.counter:self.counter+4])
        instruction = {}
        codelist = list(str(self.memory[self.counter]))
        instruction["opc"] = int(''.join(codelist[-2:]))
        for _ in range(5-len(codelist)):
            codelist.insert(0, '0')
        if instruction["opc"] in [1, 2, 7, 8]:
            instruction["op1"] = self.memory[self.counter+1] if codelist[2] == '1' else self.memory[self.memory[self.counter+1]]
            instruction["op2"] = self.memory[self.counter+2] if codelist[1] == '1' else self.memory[self.memory[self.counter+2]]
            instruction["acc"] = self.memory[self.counter+3] #if codelist[0] == '1' else self.memory[self.memory[self.counter+3]]
            self.counter += 4
            return instruction
        elif instruction["opc"] in [3, 4]:
            instruction["acc"] = self.memory[self.counter+1] #if codelist[2] == '1' else self.memory[self.memory[self.counter+1]]
            self.counter += 2
            return instruction
        elif instruction["opc"] in [5, 6]:
            instruction["op1"] = self.memory[self.counter+1] if codelist[2] == '1' else self.memory[self.memory[self.counter+1]]
            instruction["acc"] = self.memory[self.counter+2] if codelist[1] == '1' else self.memory[self.memory[self.counter+2]]
            self.counter += 3
            return instruction
        else: # instruction["opc"] == 99:
            return instruction

    def execute(self, instruction) -> None:
        # print("Instruction: ", instruction)
        if instruction["opc"] == 1:
            self.memory[instruction["acc"]] = instruction["op1"] + instruction["op2"]
        elif instruction["opc"] == 2:
            self.memory[instruction["acc"]] = instruction["op1"] * instruction["op2"]
        elif instruction["opc"] == 3:
            # self.memory[instruction["acc"]] = int(input("Give ID: "))
            # self.memory[instruction["acc"]] = self.instructions.pop(0)
            # print(self.name,"requesting input")
            self.pause = True
        elif instruction["opc"] == 4:
            #print("Diagnostic code:", self.memory[instruction["acc"]])
            self.output = self.memory[instruction["acc"]]
            # print(self.name, "outputs", self.output)
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
        else:
            print("Unknown opcode", instruction, "counter", self.counter)
            input("Pause")

class AmplifierCircuit:
    def __init__(self, phase_setting: List[int], program: List[int]):
        self.phase_setting = phase_setting
        self.input_value = 0
        self.amplifiers = []
        names = ["A", "B", "C", "D", "E"]
        for i in range(0, 5):
            computer = Computer(names[i], deepcopy(program))
            computer.run() # run until first input request
            computer.writeInput(phase_setting[i]) # input phase-setting
            computer.run() # run until second input
            self.amplifiers.append(computer) # store for later use

    def run(self):
        input_value = 0
        while not self.amplifiers[-1].halt:
            for i in range(0,5):
                self.amplifiers[i].writeInput(input_value)
                output = self.amplifiers[i].run()
                input_value = output

        return output

print('----- Program start ------')
start = time.time()
output_values = []
with open("input.txt") as file:
    program = [int(d) for d in file.readline().strip().split(",")]
    # program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    # program = [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]
    # program = [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]
    # Part 1
    for phase_setting in list(permutations([0, 1, 2, 3, 4])):
        output = AmplifierCircuit(phase_setting, program).run()
        # print(phase_setting, output)
        output_values.append(output)
    print(max(output_values))
    # Part 2
    # program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    for phase_setting in list(permutations([5, 6, 7, 8, 9])):
        output = AmplifierCircuit(phase_setting, program).run()
        # print(phase_setting, output)
        output_values.append(output)
    print(max(output_values))

print('------ completed in %s seconds -------' % str(time.time() - start))