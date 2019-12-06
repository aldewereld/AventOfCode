from typing import List, Dict
import time

class Computer:
    def __init__(self, memory: List[int] = []):
        self.memory = memory
        self.counter = 0
        self.halt = False

        self.run()

    def run(self):
        while not self.halt:
            instruction = self.decode()
            if instruction['opc'] == 99:
                self.halt = True
                continue
            self.execute(instruction)

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
            self.memory[instruction["acc"]] = int(input("Give ID: "))
        elif instruction["opc"] == 4:
            print("Diagnostic code:", self.memory[instruction["acc"]])
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

print('----- Program start ------')
start = time.time()
with open("input.txt") as file:
    program = [int(d) for d in file.readline().split(",")]
    intcomp = Computer(program)
print('------ completed in %s seconds -------' % str(time.time() - start))