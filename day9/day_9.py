from typing import List

DATA = open("day_9/data_9.txt")


from time import time as time

def move_file_blocks(l: List[str]) -> List[str]:
    # copy_list = l[::]
    left_index = 0
    right_index = len(l) - 1
    done = False
    while not done:
        # Move to the next open position to swap
        while l[left_index] != ".":
            left_index += 1
        while l[right_index] == ".":
            right_index -= 1
        # Check if we are done
        if left_index >= right_index:
            done = True
        else:
            # Now swap the two elements
            l[left_index], l[right_index] = l[right_index], l[left_index]
    return l



def swap_block(l: List[str], indices: List[int]) -> List[str]:
    lowest_right_index = indices[-1]
    done = False
    left_index = 0
    # print(f"Lowest right index: {lowest_right_index}")

    while not done: 
        while l[left_index] != "." and left_index <= lowest_right_index:
            left_index += 1
            # print(f"Left index: {left_index} < {lowest_right_index}")
        # Count the size of the block of "."
        if left_index >= lowest_right_index:
            return l
        dot_indices = []
        while l[left_index] == ".":
            dot_indices.append(left_index)
            left_index += 1

        # Check if we should swap in the first place
        # if left_index >= lowest_right_index:
        #     return l
        # Check if the block is big enough
        if len(dot_indices) >= len(indices):
            # print(f"\nWe swap {l[lowest_right_index]}")
            # print(f"The list: {l}")
            # print(f"Indices to swap: {indices}")
            # print(f"Indices of dots: {dot_indices}")
            for i in range(len(indices)):
                left_index, right_index = dot_indices[i], indices[i]
                l[left_index], l[right_index] = l[right_index], l[left_index]
            return l

    return l



def move_file_blocks_part2(l: List[str]) -> List[str]:
    right_index = len(l) - 1
    done = False
    while not done:

        # If the block doesn't get swapped, we should move until we hit a different number
        while l[right_index] == ".":
            right_index -= 1

        # Check if we are done
        if right_index <= 0:
            done = True
        else:
            # Count the length of the block
            indices_to_swap = []
            cur_num = l[right_index]
            while l[right_index] == cur_num:
                indices_to_swap.append(right_index)
                right_index -= 1
            l = swap_block(l, indices_to_swap)

    # print(l)
    return l


def checksum(l: List[str]) -> int:
    total = 0
    for i, num in enumerate(l):
        if num == ".":
            continue
        total += int(num) * i
    return total


start = time()
for line in DATA:
    disk_map = line.strip()
    disk = []
    j = 0
    for i, el in enumerate(disk_map):
        if (i % 2) != 0:
            disk += ["."] * int(el)
        else:
            disk += [f"{j}"] * int(el)
            j += 1

    # print(disk)
# print(disk)
print(len(disk))
print(checksum(move_file_blocks_part2(disk)))
print(f"TIME {time()-start:.3f}s...")
