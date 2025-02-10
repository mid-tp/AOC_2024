from typing import List
from time import time as time


data = open("day_7/data_7.txt")

# The idea is to return False if the equation is not possible
# otherwise, we'll return the number of ways to reach the target
# we need to add len(eq) - 1 operations. So if the count of the operations
# exceeds, we return False
# if we also need to check how many times we the target can be reached, we 
# can add a global variable.

def check_possibilitites(equation: List[str], target: int, number: int, index: int) -> int:
    # print(f"Number: {number}, Index: {index}, target: {target} ")
    if number == target and index == (len(equation) - 1):
        return True
    if number > target or index == len(equation) - 1:
        return False
    # Here we need to do the recursion
    # we need to make the options here
    # print(f"\nNumber: {number}, Index: {index}")
    # We do addition
    if check_possibilitites(equation, target, number + int(equation[index + 1]), index + 1):
        return True
    # We do multiplication
    # print(f"We check multiplication {number * int(equation[index + 1])}")
    if check_possibilitites(equation, target, number * int(equation[index + 1]), index + 1):
        return True
    
    if check_possibilitites(equation, target, int(str(number) + equation[index + 1]), index + 1):
        return 1
    return False


def parse():
    total = 0
    for line in data:
        splitted = line.split(":")
        target = int(splitted[0])
        equation = [i.strip() for i in splitted[-1].split(" ")][1:]
        if check_possibilitites(equation, target, int(equation[0]), 0):
            total += target
      
    print(f"Total:\n{total}")   


parse()


