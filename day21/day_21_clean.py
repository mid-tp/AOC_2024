from typing import List, Set, Dict, Tuple
from functools import cache
from itertools import product

NUMERIC_KEYPAD = [
    [7, 8, 9],
    [4, 5, 6],
    [1, 2, 3],
    ["", 0, "A"]
]

ROBOTIC_KEYPAD = [
    ["", "^", "A"],
    ["<", "v", ">"]    
]

STR_TO_KEYPAD = {"num": NUMERIC_KEYPAD, "robot": ROBOTIC_KEYPAD}
DIRS = [(0, -1), (1, 0), (-1, 0), (0, 1)]

@cache
def find_pos(char, keypad_str = "num"):
    KEYPAD = STR_TO_KEYPAD[keypad_str]
    for r, row in enumerate(KEYPAD):
        for c, cell in enumerate(row):
            if str(cell) == char:
                return (r, c)
    assert False, f"Could not find {char} in the {keypad_str} keypad..."

def manhatten(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_up_down_left_right(dr, dc):
    if dr == 0 and dc == 1:
        return ">"
    elif dr == 0 and dc == -1:
        return "<"
    elif dr == 1 and dc == 0:
        return "v"
    elif dr == -1 and dc == 0:
        return "^"
    else:
        assert False, "Invalid direction..."

def find_best_path(pos1, pos2, path, keypad_str):
    #TODO: rewrite without a global variable.
    global all_paths
    KEYPAD = STR_TO_KEYPAD[keypad_str]
    # If the code is empty, we have found a path, so we add it
    # to all the possible paths and return void
    if pos1 == pos2:
        all_paths.append(path)
        return
    r, c = pos1
    # Get the current l1 distance.
    current_dist = manhatten(pos1, pos2)
    # Move in all possible directions
    # but only if the move strictly
    # decreases the l1-distance
    for dr, dc in DIRS:
        nr, nc = r + dr, c + dc # Get the new position
        if nr < 0 or nr >= len(KEYPAD) or nc < 0 or nc >= len(KEYPAD[0]): continue # Make sure we cannot reach out of bounds
        if KEYPAD[nr][nc] == "": continue # We can never move to the empty cell, otherwise the robots get angry.
        if manhatten((nr, nc), pos2) >= current_dist: continue # Make sure the l1-distance is strictly smaller.
        to_add_to_path = get_up_down_left_right(dr, dc) # Get the string value that we need to make the path, from the dr, dc
        if (nr, nc) == pos2:
            to_add_to_path += "A" # If we reach the final position, we need to press it.
        # print(f"\n\nCurrent position is {nr, nc} \npath {path} \ncode {code}")
        find_best_path((nr, nc), pos2, path + to_add_to_path, keypad_str=keypad_str) 
    return all_paths


# Create lookup table what are the best ways to go from one number to another
best_path_numkey = {}
all_positions_num = [(r, c) for r, row in enumerate(NUMERIC_KEYPAD) for c, cell in enumerate(row) if cell != ""]
for pos1 in all_positions_num:
    for pos2 in all_positions_num:
        el1, el2 = NUMERIC_KEYPAD[pos1[0]][pos1[1]], NUMERIC_KEYPAD[pos2[0]][pos2[1]]
        all_paths = [] 
        if pos1 == pos2:
            best_path_numkey[(str(el1), str(el2))] = ["A"]
            continue
        best_path_numkey[(str(el1), str(el2))] = find_best_path(pos1, pos2, "", "num")

# Create lookup table to see what the best way is to go from one direction to another in the robotic keypad

best_path_robotkey = {}
all_positions_robot = [(r, c) for r, row in enumerate(ROBOTIC_KEYPAD) for c, cell in enumerate(row) if cell != ""]
for pos1 in all_positions_robot:
    for pos2 in all_positions_robot:
        el1, el2 = ROBOTIC_KEYPAD[pos1[0]][pos1[1]], ROBOTIC_KEYPAD[pos2[0]][pos2[1]]
        all_paths = [] 
        if pos1 == pos2:
            best_path_robotkey[(str(el1), str(el2))] = ["A"]
            continue
        best_path_robotkey[(str(el1), str(el2))] = find_best_path(pos1, pos2, "", "robot")

@cache
def get_best_num_paths(pos1, pos2):
    return best_path_numkey[(str(pos1), str(pos2))]

@cache
def get_best_robot_paths(pos1, pos2):
    return best_path_robotkey[(str(pos1), str(pos2))]

@cache
def get_best_path(pos1, pos2, keypad_str):
    if keypad_str == "num":
        return get_best_num_paths(pos1, pos2)
    elif keypad_str == "robot":
        return get_best_robot_paths(pos1, pos2)
    else:
        assert False, "Invalid keypad_str"

# Produce all the possible paths between the elements
# on the numeric keypad.
# Made a different function for this also, but this one
# is a bit more readable.
def get_path_num(code):
    code = "A" + code
    all_paths = []
    for i in range(len(code) - 1):
        current_pos = code[i]
        next_pos = code[i + 1]
        all_paths.append(get_best_num_paths(current_pos, next_pos))
    combinations = ["".join(combo) for combo in list(product(*all_paths))]
    return combinations


# Setting up the recursion was the most tricky part for me.
@cache
def get_shortest_path(pos1, pos2, depth, keypad_str: str):
    if depth == 0:
        assert keypad_str == "robot", "Depth can only be 0 for the robot keypad"
        a = min([len(path) for path in get_best_path(pos1, pos2, keypad_str)]) 
        return a
    # Call the same func with depth - 1
    # Get all the possible paths from pos1 to pos2 
    paths = get_best_path(pos1, pos2, keypad_str)
    min_score = float('inf')
    for path in paths:
        path = "A" + path
        score = 0
        for i in range(len(path) - 1):
            score += get_shortest_path(path[i], path[i + 1], depth - 1, "robot")
        min_score = min(min_score, score)
    return min_score

def part2(code: str, depth=2):
    value = int(code.split("A")[0])
    code = "A" + code
    total_length = 0
    for i in range(len(code) - 1):
        total_length += get_shortest_path(code[i], code[i + 1], depth, "num")
    print(f"{total_length} * {value}")
    return total_length * int(value)

data = open("day_21/data_21.txt")
total = 0
for line in data:
    print(f"Parsing {line}")
    # total += part2(line.strip(), depth=2)
    total += part2(line.strip(), depth=25)
print(total)




