from typing import List, Tuple
from collections import Counter
from time import time as time


start = time()
# revision of day 15, without numpy, plain python.
# UPDATES: parsing of data easier. 
# Getting the boxes is easier.
# Naming the variables is done differently, now we don't have too many confusing methods. 
# Better and easier logic is implemented.
# One could use recursion to find all the neighbouring boxes, I might try that here, too.

data =  open("day_15/data_15.txt")

# Parsing the grid, can be done in a cleaner way
grid_str, instructions_str = data.read().split("\n\n")
grid = [list(row) for row in grid_str.split("\n")]
moves = "".join(instructions_str.split("\n"))

moves_to_directions = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
# We do need to loop over the grid to find the current position of @
done = False
for i, row in enumerate(grid):
    for j, val in enumerate(row):
        if val == "@":
            cr, cc = i, j
            done = True
            break
    if done:
        break

def print_grid(grid):
    for row in grid:
        print("".join(row))



for move in moves:
    # This is a bit easier to read, with row and column
    make_move = True
    positions_to_move = []
    dr, dc = moves_to_directions[move]
    queue = [(cr, cc)]
    while queue:
        r, c = queue.pop(0)
        positions_to_move.append((r, c))
        nr, nc = r + dr, c + dc
        if grid[nr][nc] == "#":
            # we cannot make the move
            make_move = False
            positions_to_move = []
            break
        elif grid[nr][nc] == ".":
            continue
            # break out of the while True
        elif grid[nr][nc] == "O":
            queue.append((nr, nc))
        else:
            assert False

    # Make a copy of the grid
    if not make_move: continue


    copy_grid = [list(row) for row in grid]
    for r, c in positions_to_move:
        # First, we want to set all the current position to "."
        grid[r][c] = "."
    for r, c in positions_to_move:
        grid[r + dr][c + dc] = copy_grid[r][c]
    # Update where we are currently
    cr, cc = cr + dr, cc + dc



score = sum(list(r * 100 + c for r, row in enumerate(grid) for c, val in enumerate(row) if val == "O"))
print(score)
print(f"Time: {time() - start:.4f}")