from typing import List, Set, Tuple, Dict
import numpy as np
data = open("day_12/data_12.txt")
from collections import Counter

GRID = []

for line in data:
    l = []
    for c in line.strip():
        l.append(c)
    GRID.append(l)
GRID = np.array(GRID)
# print(GRID)


# Loop over all the indices and check if this index 
# is already added to a clique



def get_clique(i: int, j: int) -> Set[Tuple[int, int]]:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    clique = set()
    queue = [(i, j)]
    char = GRID[i][j]
    # print(f"{GRID[i][j]}, {clique}")
    # Check all the directions
    while len(queue) > 0:
        cur_pos = queue.pop(0)
        cur_i, cur_j = cur_pos
        for dir in directions:
            new_pos = (cur_i + dir[0], cur_j + dir[1])
            if new_pos[0] < 0 or new_pos[0] >= GRID.shape[0] or new_pos[1] < 0 or new_pos[1] >= GRID.shape[1]:
                continue
            if GRID[new_pos[0]][new_pos[1]] == char:
                if new_pos in clique:
                    continue
                queue.append(new_pos)
                clique.add(new_pos)

        # print(queue)

    if len(clique) == 0:
        clique.add((i, j))
    return clique

def get_all_cliques(grid: np.array = GRID) -> Dict[str, List[Set[Tuple[int, int]]]]:
    char_to_cliques = {}
    for i in range(GRID.shape[0]):
        for j in range(GRID.shape[1]):
            char = GRID[i][j]
            if char not in char_to_cliques.keys():
                char_to_cliques[char] = []
            # Loop over the current cliques that this character can be in
            add = True
            for clique in char_to_cliques[char]:
                # Check if the current index is in the clique
                if (i, j) in clique:
                    add = False
                    break
            if add:
                # If it is not in any clique, add it to a new clique
                clique = get_clique(i, j)
                # print(f"We add the cluque {clique}")
                char_to_cliques[char].append(clique)

    return char_to_cliques

       

# Calculate the number of fences
def number_fences(clique: Set[Tuple[int, int]]) -> int:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    fences = 0
    for pos in clique:
        i, j = pos
        for dir in directions:
            new_pos = (i + dir[0], j + dir[1])
            if new_pos not in clique:
                fences += 1
    return fences

# Check if we should add the border on all four sides.

def check_border_up(pos, clique) -> int:
    i, j = pos
    if (i - 1, j) in clique:
        return 0
    # Check if it has a right neighbour
    if (i, j + 1) in clique:
        # We have a right neighbour
        # If both neighbours have an element on top of them, we add the border
        if (i - 1, j + 1) not in clique:
            return 0
        return 1

    # print(f"Border up {pos}")
    return 1

def check_border_down(pos, clique):
    i, j = pos
    if (i + 1, j) in clique:
        return 0
    # Check if has a right neighbour
    if (i, j + 1) in clique:
        # If the right neighbour has an element below it, do not add the border
        if (i + 1, j + 1) not in clique:
            return 0
    # print(f"Border down {pos}")
    return 1


def check_border_left(pos, clique):
    i, j = pos
    if (i, j - 1) not in clique and (i + 1, j) not in clique:
        # print(f"+border left {pos}")
        return 1
    if (i, j - 1) not in clique and (i + 1, j) in clique and (i + 1, j - 1) in clique:
        # print(f"+border left {pos}")
        return 1
    return 0


def check_border_right(pos, clique):   
    i, j = pos
    if (i, j + 1) not in clique and (i + 1, j) not in clique:
        # print(f"+border right {pos}")
        return 1
    if (i, j + 1) not in clique and (i + 1, j) in clique and (i + 1, j + 1) in clique:
        # print(f"+border right {pos}")
        return 1
    return 0


def num_sides(clique: Set[Tuple[int, int]]) -> int:
    total = 0
    # print(clique)
    for pos in clique:
        total += check_border_up(pos, clique)
        total += check_border_down(pos, clique)
        total += check_border_left(pos, clique)
        total += check_border_right(pos, clique)
        # print("---------------------------")

    # print(f"Num sides:")
    # print(total)
    return total
# print(char_to_cliques)

total = 0
part1 = False
char_to_cliques = get_all_cliques()

for char in char_to_cliques.keys():
    # if (str(char) != "B"):
    #     continue
    # print(f"\n---------------------")
    # print(char)
    # print(f"\nChar {char} has {len(char_to_cliques[char])} cliques")  
    for clique in char_to_cliques[char]:
        # print(clique)
        # print(f"Number of fences: {number_fences(clique)}")
        if part1:
            num_fence = number_fences(clique)
            # print(f"{char}: #fences * area = {num_fence} * {len(clique)}")
            total += num_fence * len(clique)
        else:
            sides = num_sides(clique)
            # print(f"{char}: #sides * area = {sides} * {len(clique)} = {sides * len(clique)}")
            total += sides * len(clique)
        

        

print(total)


