from typing import List, Tuple, Set
import numpy as np
data = open("day_8/data_8.txt")

GRID = []
for line in data:
    temp = []
    for i in line.strip():
        temp.append(i)
    GRID.append(temp)
GRID = np.array(GRID)
# print(GRID)

freq_to_coords = {}

# Get the coordinates of each frequency
for i in range(GRID.shape[0]):
    for j in range(GRID.shape[1]):
        if GRID[i][j] == "." or GRID[i][j] == "#":
            continue
        if GRID[i][j] not in freq_to_coords.keys():
            freq_to_coords[GRID[i][j]] = []
        freq_to_coords[GRID[i][j]].append((i, j))

# print(freq_to_coords)


def distance(c1: Tuple[int, int], c2: Tuple[int, int]) -> Tuple[int, int]:
    return (c2[0] - c1[0], c2[1] - c1[1])

def check_options(c1: Tuple[int, int], c2: Tuple[int, int], part2: bool = False) -> List[Tuple[int, int]]:
    dist_x, dist_y = distance(c1, c2)
    # gets the distance from c1 to c2
    assert dist_x != 0 or dist_y != 0
    if part2:
        options = []
        # just add a bunch of antennas in the same line.
        # We just add like 20 orso, and filter out what we do not need
        for i in range(1, 100):
            options.append((c1[0] - dist_x * i, c1[1] - dist_y * i))
            options.append((c2[0] + dist_x * i, c2[1] + dist_y * i))
        return options
    return [(c1[0] - dist_x, c1[1] - dist_y), (c2[0] + dist_x, c2[1] + dist_y)]


antidote_options = []
# Part 1 
part2 = True
# Now do a loop over all the pairs of frequencies that we have
for freq in freq_to_coords.keys():
    if len(freq_to_coords[freq]) == 1:
        # If an element appears once, we cannot add antidotes
        continue
    # Now loop between all the pairs
    coors = freq_to_coords[freq]
    for i in range(len(coors)):
        for j in range(i + 1, len(coors)):
            c1 = coors[i]
            c2 = coors[j]
            # print(f"\n\nChecking {c1} and {c2}")
            dist_x, dist_y = distance(c1, c2)
            # print(f"Distance between {c1} and {c2} is {dist_x}, {dist_y}")
            # Check if the antidote is possible
            possible_options = check_options(c1, c2, part2=part2)
            # print(f"Possible options are {possible_options}")
            # Check if the options are within the bounds of the grid
            for option in possible_options:
                if option[0] >= 0 and option[0] < GRID.shape[0] and option[1] >= 0 and option[1] < GRID.shape[1]:
                    # print(f"--> Possible option is {option}")   
                    antidote_options.append(option)


for key in freq_to_coords.keys():
    antidote_options += freq_to_coords[key]
print(f"Total number of options: {len(set(antidote_options))}")


# # Rebuild the grid, see where the mistake is 
# NEW_GRID = np.array(GRID.shape)
# NEW_GRID = np.full(GRID.shape, ".", dtype=str) 


# # Now add the frequencies
# for key in freq_to_coords.keys():
#     for coor in freq_to_coords[key]:
#         NEW_GRID[coor[0]][coor[1]] = key
# # Now add the antidotes
# for coor in antidote_options:
#     NEW_GRID[coor[0]][coor[1]] = "#"

# print(NEW_GRID)
# # Part 2
# print("--------------------------")
# print(GRID)

# indices_diff = []
# for i in range(GRID.shape[0]):
#     for j in range(GRID.shape[1]):
#         if GRID[i][j] != NEW_GRID[i][j]:
#             indices_diff.append((i, j))
# print(indices_diff)
# print(freq_to_coords)