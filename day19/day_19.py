from typing import List

data = open("day_19/data_19.txt")
from functools import lru_cache

TOWEL_OPTIONS = []
to_make = []
i = 0

# Preprocessing 
for line in data:
    if i == 0:
        for j in line.split():
            if "," in j:
                TOWEL_OPTIONS.append(j[:-1])
            else:
                TOWEL_OPTIONS.append(j)
    else:
        to_make.append(line.strip())
    i += 1
to_make = to_make[1:]


# print(TOWEL_OPTIONS)
# print(to_make)

# looks like a recursion to me
# just backtrack on the possible options

            
# So we need to find a method that does backtrack but doesn't return the 
# False if we hit a wrong path. We should also make some table that
# keeps track of the patterns that are not possible.
num_options = dict()


def find_pattern(str_remaning: str) -> bool:
    global num_options
    # print(f"\n\n**** CHECKGING {str_remaning} ****")
    # First check if we have seen this option before
    # If we have, we do not need to compute the whole thing again.
    if str_remaning in num_options.keys():
        return num_options[str_remaning]
    if len(str_remaning) == 0:
        # print(f"We found a solution")
        return 1
    else:
        # The total number of ways for this substring starts at 0
        num_ways = 0

        # Loop over the possible options and slice off the part that can be fitted and pass 
        # on the remaining pattern to the same function
        for towel in TOWEL_OPTIONS:
            # Check if the towel can be fitted
            # print(pattern[:len(towel)], towel)
            if str_remaning[:len(towel)] == towel:
                # print(f"{towel} can be fitted in {str_remaning}")
                num_ways += find_pattern(str_remaning[len(towel):])

        # Add the number of ways to the dictionary
        num_options[str_remaning] = num_ways
        return num_ways


num_possible = 0
total_possibilities = 0
for pattern in to_make:
    # if pattern != "bwurrg":
    #     continue
    ways = find_pattern(pattern)
    if ways > 0:
        num_possible += 1
        total_possibilities += ways 

part1 = False
if part1:
    print(f"Number of possible patterns: {num_possible}")
else:
    print(f"Number of possible patterns: {num_possible}")
    print(f"Total number of ways to make the patterns: {total_possibilities}")






















# Tryout: but too slow

# # @lru_cache(maxsize=None)
# def find_pattern(str_remaning: str) -> bool:
#     global TOTAL
#     print(f"\n\n**** CHECKGING {str_remaning} ****")
#     if len(str_remaning) == 0:
#         # We found the solution
#         # print(f"We found a solution")
#         TOTAL += 1
#         return True
#     # Loop over the possible options and slice off the part that can be fitted and pass 
#     # on the remaining pattern to the same function
#     for towel in TOWEL_OPTIONS:
#         # Check if the towel can be fitted
#         print(str_remaning[:len(towel)], towel)
#         if str_remaning[:len(towel)] == towel:
#             print(f"{towel} can be fitted in {str_remaning}")
#             return find_pattern(str_remaning[len(towel):])

#     return False


# TOTAL = 0

# @lru_cache(maxsize=None)
# def find_pattern(str_remaning: str) -> bool:
#     print(f"\n\n**** CHECKGING {str_remaning} ****")
#     if len(str_remaning) == 0:
#         # We found the solution
#         # print(f"We found a solution")
#         return True
#     else:
#         # Loop over the possible options and slice off the part that can be fitted and pass 
#         # on the remaining pattern to the same function
#         for towel in TOWEL_OPTIONS:
#             # Check if the towel can be fitted
#             print(pattern[:len(towel)], towel)
#             if str_remaning[:len(towel)] == towel:
#                 print(f"{towel} can be fitted in {str_remaning}")
#                 find_pattern(str_remaning[len(towel):])

# def check_start_in_towels(pattern: str):
#     options = []
#     for towel in TOWEL_OPTIONS:
#         # print(pattern[:len(towel)], towel)
#         if pattern[:len(towel)] == towel:
#             options.append(pattern[len(towel):])        
#     if len(options):
#         # print(f"Options: {options}")
#         return True, options
#     return False, False


# def check_pattern(pattern: str) -> bool:
#     queue = [pattern]
#     num_options = 0
#     done = False
#     while len(queue) and not done > 0:
#         # print(f"\nNew pattern {queue[0]}")
#         pattern = queue.pop(0)
#         possible, new_pattern = check_start_in_towels(pattern)
#         if possible:
#             for p in new_pattern:
#                 if len(p) == 0:
#                     num_options += 1
#                     done = True
#                 else:
#                     queue.append(p)
#         # print(f"Queue: {queue}")
#     return num_options

# TOTAL = 0
# num_possible = 0
# for pattern in to_make:
#     # if pattern != "bwurrg":
#     #     continue
#     if check_pattern(pattern) > 0:
#         num_possible += 1
#     else:
#         print(f"Pattern {pattern} is not possible")

# print(f"Number of possible patterns: {num_possible}")



