from typing import List, Set, Dict, Tuple

data = open("day_25/data_25.txt")

keys_locks = data.read().split("\n\n")

key_heights = []
lock_heights = []

for keys_lock in keys_locks:
    temp = [list(row) for row in keys_lock.split("\n")]
    for row in temp:
        print(row)
    heights = []
    # In case we have a lock
    if temp[0] == ["."] * len(temp[0]):
        for j, col in enumerate(temp[0]):
            for i, row in enumerate(temp):
                if temp[len(temp) - 1 - i][j] == ".":
                    heights.append(i - 1)
                    break
        # keys.append(temp)
        lock_heights.append(heights) 
    else:
        # a key, no need to change the heights.
        for j, col in enumerate(temp[0]):
            for i, row in enumerate(temp):
                if temp[i][j] == ".":
                    heights.append(i - 1)
                    break
        # locks.append(temp)
        key_heights.append(heights)
    print(heights)

num_matches = 0
for key_height in key_heights:
    for lock_height in lock_heights:
        if len([kh + lh for kh, lh in zip(key_height, lock_height) if kh + lh >= 6]) > 0: continue
        num_matches += 1

print(num_matches)
        