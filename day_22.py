from typing import List, Set, Tuple, Dict
import math
from time import time as time
from functools import cache
from collections import defaultdict
from collections import Counter

# It took a little while to realize how much can be done in one loop over the data.
# Part 1 is very straightforward, part 2 took a little while to realize an efficient way.
# I've read there are more efficient ways (at least shorter running time). I'll look
# at those later.

start = time()
data = open("day_22/data_22.txt")

NUMBERS = [int(el) for el in data.read().split("\n")]

def mix(n1: int, n2: int) -> int:
    return n1 ^ n2

def prune(n1: int):
    return n1 % 16777216

def prune_mix(n1, n2):
    return prune(mix(n1, n2))

def calculate_next_secret_number(secret_num: int) -> int:
    step_1 = prune_mix(secret_num, secret_num * 64)
    step_2 = prune_mix(step_1, step_1 // 32) 
    return prune_mix(step_2, step_2 * 2048) 


def part1():
    number_2000 = []
    for line in data:
        num = int(line.strip())
        next_num = num
        for i in range(2000):
            next_num = calculate_next_secret_number(next_num)
            if i == 1999:
                number_2000.append(next_num)
            
    print(sum(number_2000))


def one_loop_part2(numbers=NUMBERS):
    changes_to_bananas = {}
    changes_to_bananas = defaultdict(lambda: 0)
    for num in numbers:
        next_num = num
        four_changes = []
        seen_changes = set()
        for _ in range(2000):
            # Compute the difference in the last digit.
            prev_num = int(str(next_num)[-1])
            next_num = calculate_next_secret_number(next_num)
            last_digit_next_num = int(str(next_num)[-1])
            diff = last_digit_next_num - prev_num
            four_changes.append(diff)
            if len(four_changes) == 4: 
                # Remove one element
                if tuple(four_changes) not in seen_changes: changes_to_bananas[tuple(four_changes)] += last_digit_next_num
                seen_changes.add(tuple(four_changes))
                four_changes = four_changes[1:]
    print(max(changes_to_bananas.values()))
    # # Get the max, maybe this can be a one liner, but ah well
    # max_bananas = float('-inf')
    # max_change = None
    # for changes in changes_to_bananas.keys():
    #     if changes_to_bananas[changes] > max_bananas:
    #         max_bananas = changes_to_bananas[changes] 
    #         max_change = changes
    # print(f"\n\nDone...")
    # print(f"pattern {max_change}")
    # print(f"Bananas {max_bananas}")


one_loop_part2()
print(f"Time {time() - start: .4f}")