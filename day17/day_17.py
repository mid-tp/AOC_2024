from typing import List, Set, Dict, Tuple
from time import time as time 
data = open("day_17/data_17.txt")

from dataclasses import dataclass

@dataclass
class Register:
    _name: str
    _value: int = float('inf')

    @property
    def value(self) -> int:
        return self._value
    
    @value.setter
    def value(self, value: int):
        self._value = value

    @property
    def name(self) -> str:
        return self._name
    

class Program:
    def __init__(self):
        # Read data, register and instructions
        self.pointer: int = 0
        self.set_pointer: bool = False
        self.out_str: str = ""
        self.read_data()


    def read_data(self) -> None:
        data = open("day_17/data_17.txt")
        register_data, instructions_data = data.read().split("\n\n")
        self.registers = {}
        # Read out the registers  
        for register in register_data.split("\n"):
            name, value = register.split(": ")
            self.registers[name[-1]] = Register(name[-1], int(value))
        # Read out the instructions
        instructions_data = instructions_data.split(": ")[-1].split(",")
        self.instructions = [int(i) for i in instructions_data]
        self.len_instructions = len(self.instructions)
        self.out_str = ""
        self.pointer = 0

    def reset_variables(self):  
        self.pointer = 0
        self.set_pointer = False
        self.out_str = ""
        self.registers["A"].value = 0
        self.registers["B"].value = 0
        self.registers["C"].value = 0

    def move_pointer(self, value:int = 2):
        self.pointer += value

    def get_combo_operand(self, operand: int) -> int:
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.registers["A"].value    
        elif operand == 5:
            return self.registers["B"].value
        elif operand == 6:
            return self.registers["C"].value
        elif operand == 7:
            assert False, "Invalid program. Operand cannot be 7..."
        else:
            assert False, "Invalid program. Operand cannot be greater than 7..."

    def run_opcode_operand(self, opcode: int, operand: int):
        if opcode == 0:
            self.adv(operand)
        elif opcode == 1:
            self.bxl(operand)
        elif opcode == 2:
            self.bst(operand)
        elif opcode == 3:
            self.jnz(operand)
        elif opcode == 4:
            self.bxc()
        elif opcode == 5:
            self.out(operand)
        elif opcode == 6:
            self.bdv(operand)
        elif opcode == 7:
            self.cdv(operand)
        else:
            assert False, "Invalid opcode..."


    def adv(self, operand: int):
        val = self.get_combo_operand(operand)
        self.registers["A"].value = self.registers["A"].value // 2 ** val

    def bxl(self, operand: int):
        self.registers["B"].value = self.registers["B"].value ^ operand 

    def bst(self, operand: int):
        val = self.get_combo_operand(operand)
        self.registers["B"].value = val % 8

    def jnz(self, operand: int):
        assert not self.set_pointer, "The pointer should always be False when calling this function"
        if self.registers["A"].value != 0:
            self.pointer = operand
            self.set_pointer = True

    def bxc(self: int):
        self.registers["B"].value = self.registers["B"].value ^ self.registers["C"].value

    def out(self, operand: int):
        val = self.get_combo_operand(operand) % 8
        for c in str(val):
            self.out_str += c + ","

    def bdv(self, operand: int):
        val = self.get_combo_operand(operand)
        self.registers["B"].value = self.registers["A"].value // 2 ** val

    def cdv(self, operand: int):
        val = self.get_combo_operand(operand)
        self.registers["C"].value = self.registers["A"].value // 2 ** val
    
    def run_instructions(self):
        while True:
            if self.pointer >= self.len_instructions:
                break
            # Get the opcode and the operand
            opcode, operand = self.instructions[self.pointer], self.instructions[self.pointer + 1]
            self.run_opcode_operand(opcode, operand)
            if self.set_pointer:
                self.set_pointer = False
                continue
            self.move_pointer(2)
        # print(self.out_str[:-1])


    def part2(self):
        """
            Work backwards from the output to get the input
        """
        possible_inputs = [i for i in range(25)]
        done = False
        j = 0
        possible_inputs = [0]
        new_possible_inputs = [0]
        while not done:
            possible_inputs = list(new_possible_inputs) # create a new instance of the list to avoid weird behaviour
            new_possible_inputs = []
            print(possible_inputs)
            for input in possible_inputs:
                for offset in range(8):
                    self.reset_variables()
                    self.registers["A"].value = input + offset
                    self.run_instructions()
                    output = [int(i) for i in self.out_str[:-1].split(",")]
                    if output == self.instructions[-len(output):]:
                        new_possible_inputs.append((input + offset) << 3)
                        # new_possible_inputs.append((input + offset) * 8)
                    if output == self.instructions:
                        print(f"Found the value: {input + offset}")
                        return
        print(new_possible_inputs)

P = Program()
# P.run_instructions()
P.part2()

# Brute force isn't really cutting it here. Have to find 
# a better way of doing it. Look at the periocidity of the
# outcome and try to detect a pattern...

# Checking value: 23_400_000 in 776.09406 seconds
# 23 mil values in in approx 12 minutes

# Okat this solution was absolutely brutal.
# Without hints online I would have not been able to solve this.


