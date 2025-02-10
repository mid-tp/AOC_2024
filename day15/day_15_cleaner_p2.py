from typing import List, Tuple
from collections import Counter
from time import time as time

start = time()

# revision of day 15, without numpy, 'plain python'.
# UPDATES: parsing of data easier. 
# Getting the boxes is easier.
# Naming the variables is done differently, now we don't have too many confusing methods. 
# Better and easier logic is implemented.
# One could use recursion to find all the neighbouring boxes, I might try that here, too.

def print_grid(grid):
    for row in grid:
        print("".join(row))

data =  open("day_15/data_15.txt")

# Parsing the grid, can be done in a cleaner way
grid_str, instructions_str = data.read().split("\n\n")
grid = [list(row) for row in grid_str.split("\n")]
moves = "".join(instructions_str.split("\n"))

# We need to change the grid to another grid
changed_values = {".": "..", "O": "[]", "@": "@.", "#": "##"}


# The naive way
grid2 = []
for r, row in enumerate(grid):
    new_row = []
    for c, val in enumerate(row):
        v1, v2 = changed_values[val]
        new_row.append(v1)
        new_row.append(v2)
    grid2.append(new_row)

# The 'cleaner' way
grid2 = []
for r, row in enumerate(grid):
    new_row = []
    for c, val in enumerate(row):
        new_row.extend(changed_values[val])
    grid2.append(new_row)

# The one-liner way, not so easy to read... 
grid2 = []
grid2 = [[char for val in row for char in changed_values[val]] for row in grid]
grid = grid2


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

 
for move in moves:
    # print_grid(grid)
    # print(move)
    # print()
    # This is a bit easier to read, with row and column
    make_move = True
    positions_to_move = [(cr, cc)]
    dr, dc = moves_to_directions[move]
    queue = [(cr, cc)]
    i = 0
    seen = set()
    while queue:
        i += 1
        r, c = queue.pop(0)
        nr, nc = r + dr, c + dc
        if grid[nr][nc] == "#":
            # we cannot make the move
            make_move = False
            positions_to_move = []
            break
        elif grid[nr][nc] == ".":
            # In this case we should check every element in the queue as the boxes might go into "." and "#" at the same time, which means we cannot move.
            continue
        # If go into a part of a box, add the other side to the queue as well
        elif grid[nr][nc] == "[":
            if (nr, nc) in seen and (nr, nc + 1) in seen:
                continue
            queue.append((nr, nc))
            # Also add the other part of the block
            queue.append((nr, nc + 1))
            # Remember which elements we have seen so that we do not add them twice.
            seen.add((nr, nc))
            seen.add((nr, nc + 1))
            # Add to the positions to move
            positions_to_move.append((nr, nc))
            positions_to_move.append((nr, nc + 1))
        elif grid[nr][nc] == "]":
            if (nr, nc) in seen and (nr, nc - 1) in seen:
                continue
            queue.append((nr, nc))
            # Also add the other part of the block
            queue.append((nr, nc - 1))
            # Remember which elements we have seen so that we do not add them twice.
            seen.add((nr, nc))
            seen.add((nr, nc - 1))
            # Add to the positions to move
            positions_to_move.append((nr, nc))
            positions_to_move.append((nr, nc - 1))
        else:
            assert False
    # Make a copy of the grid
    if not make_move: continue

    copy_grid = [list(row) for row in grid]
    for r, c in positions_to_move:
        # First, we want to set all the current position to "."
        grid[r][c] = "."
    for r, c in positions_to_move:
        # Move all the objects that need to be moved.
        grid[r + dr][c + dc] = copy_grid[r][c]
    # Update where we are currently
    cr, cc = cr + dr, cc + dc


score = sum(list(r * 100 + c for r, row in enumerate(grid) for c, val in enumerate(row) if val == "["))
print(score)
print(f"Time: {time() - start:.4f}")