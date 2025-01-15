from typing import List

data = open("day_11/data_11.txt")

from functools import lru_cache


# We don't actually care about the values of the stones that are being split.
# We just want to know _how many_ stones there are in the end.
# we can pair the value with the number of steps left. Then do recursion....
# But this recursion seems to be a bit too slow still...
from time import time as time

@lru_cache(maxsize=None)
def change(num: int, num_steps: int):
    if num_steps == 0:
        return 1
    # Here we should determine what we do with the number.
    # We always call the same function with one step less.
    if num == 0:
        return change(1, num_steps - 1)
    elif len(str(num)) % 2 == 0:
        # Split up the number in two parts
        num1 = int(str(num)[:len(str(num)) // 2])
        num2 = int(str(num)[len(str(num)) // 2:])
        return change(num1, num_steps - 1) + change(num2, num_steps - 1)
    else:
        return change(num * 2024, num_steps - 1)


blinks = 75
start = time()
for line in data:
    nums = line.split(" ")
    print(nums)
    total = 0
    for num in nums:
        total += change(int(num), blinks)


print(f"Total is: {total}\n#{blinks} blinks...")   
print(f"Took {time() - start:.4f} seconds...")



