from typing import List, Tuple
import numpy as np
from PIL import Image
from collections import Counter
data = open("day_14/data_14.txt")

GRID_SIZE_TEST = (103, 101)
GRID_SIZE = (103, 101)

GRID_TEST = np.array([["." for _ in range(GRID_SIZE_TEST[1])] for _ in range(GRID_SIZE_TEST[0])])
GRID  = np.array([["." for _ in range(GRID_SIZE[1])] for _ in range(GRID_SIZE[0])])
# Stub implementation


ROBOTS: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []

for line in data:
    p, v = line.strip().split(" ")
    # print(line.strip())
    n_p, n_v = p.split("=")[1].split(","), v.split("=")[1].split(",")
    i_robot, j_robot = int(float(n_p[-1])), int(float(n_p[0]))
    # print(f"Robot position: {i_robot, j_robot}")
    v_i, v_j = int(float(n_v[-1])), int(float(n_v[0]))
    # print(f"Robot velocity: {v_i, v_j}\n")
    ROBOTS.append(((i_robot, j_robot), (v_i, v_j)))

def loop(num_steps: int, pos: Tuple[int, int], velocity: Tuple[int, int]) -> Tuple[int, int]:
    # Simulate the positions of the robot
    # check if out of bounds etc. etc.
    # Indicate the position of the robot on the grid
    # print(GRID_TEST.shape)
    # GRID_TEST[pos[0]][pos[1]] = "#"
    # print(GRID_TEST)
    for _ in range(num_steps):
        pos = (
            (pos[0] + velocity[0]) % GRID_SIZE_TEST[0],
            (pos[1] + velocity[1]) % GRID_SIZE_TEST[1]
            )
        
        # print(f"new position: {pos}")   
        # # Print on the grid
        # GRID_TEST[pos[0]][pos[1]] = "#"
        # # Reset the previous position
        # GRID_TEST[prev_pos[0]][prev_pos[1]] = "."
        # print(GRID_TEST) 
        # print("-------------------------------------------")
    return pos


def print_grid(grid: np.array) -> None:
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            print(grid[i][j], end="")
        print("\n")

def get_safety_score(iter: int) -> int:
    GRID_TEST = np.array([["." for _ in range(GRID_SIZE_TEST[1])] for _ in range(GRID_SIZE_TEST[0])])
    positions = []
    for robot in ROBOTS:
        positions.append(loop(iter, *robot))

    # Then find the quadrants and multiply the outcome
    c = Counter(positions)
    for pos in c.keys():
        i, j = pos
        GRID_TEST[i][j] = c[pos]
    # Now just get the 4 quadrants, anc dount the number of nonzero elements.
    # TODO:
    q1 = GRID_TEST[:GRID_SIZE_TEST[0] //2, :GRID_SIZE_TEST[1] // 2]
    q2 = GRID_TEST[:GRID_SIZE_TEST[0] //2, 1 + GRID_SIZE_TEST[1] // 2:]
    q3 = GRID_TEST[1 + GRID_SIZE_TEST[0] //2:, :GRID_SIZE_TEST[1] // 2]
    q4 = GRID_TEST[1 + GRID_SIZE_TEST[0] //2:, 1 + GRID_SIZE_TEST[1] // 2:]
    # Sum over the quadrants of the result
    total = 1
    for q in [q1, q2, q3, q4]:
        sum_q = 0
        for i in range(q.shape[0]):
            for j in range(q.shape[1]):
                if q[i][j] != ".":
                    sum_q += int(q[i][j])
        total *= sum_q

    return total, GRID_TEST


def to_text(grid) -> str:
    text = ""
    grid[grid == "."] = " "
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if str(grid[i][j]) != " ":
                text += "#"
            else:
                text += " "
        text += "\n"
    return text


def loop2(num_steps: int):
    # Simulate the positions of the robot
    # check if out of bounds etc. etc.
    # Indicate the position of the robot on the grid
    # print(GRID_TEST.shape)
    # GRID_TEST[pos[0]][pos[1]] = "#"
    # print(GRID_TEST)
    positions_after_iter = dict()
    for robot in ROBOTS:
        pos, velocity = robot
        for i in range(0, num_steps):
            pos = (
                (pos[0] + velocity[0]) % GRID_SIZE_TEST[0],
                (pos[1] + velocity[1]) % GRID_SIZE_TEST[1]
                )
            if (i + 1) in positions_after_iter.keys():
                positions_after_iter[i + 1].append(pos)
            else:
                positions_after_iter[i + 1] = [pos]
        
        # print(f"new position: {pos}")   
        # # Print on the grid
        # GRID_TEST[pos[0]][pos[1]] = "#"
        # # Reset the previous position
        # GRID_TEST[prev_pos[0]][prev_pos[1]] = "."
        # print(GRID_TEST) 
        # print("-------------------------------------------")
    return positions_after_iter

def find_score_from_positions(positions: dict) -> int:
    # Then find the quadrants and multiply the outcome
    c = Counter(positions)
    for pos in c.keys():
        i, j = pos
        GRID_TEST[i][j] = c[pos]
    # Now just get the 4 quadrants, anc dount the number of nonzero elements.
    # TODO:
    q1 = GRID_TEST[:GRID_SIZE_TEST[0] //2, :GRID_SIZE_TEST[1] // 2]
    q2 = GRID_TEST[:GRID_SIZE_TEST[0] //2, 1 + GRID_SIZE_TEST[1] // 2:]
    q3 = GRID_TEST[1 + GRID_SIZE_TEST[0] //2:, :GRID_SIZE_TEST[1] // 2]
    q4 = GRID_TEST[1 + GRID_SIZE_TEST[0] //2:, 1 + GRID_SIZE_TEST[1] // 2:]
    # Sum over the quadrants of the result
    total = 1
    for q in [q1, q2, q3, q4]:
        sum_q = 0
        for i in range(q.shape[0]):
            for j in range(q.shape[1]):
                if q[i][j] != ".":
                    sum_q += int(q[i][j])
        total *= sum_q
    print(f"Total score is {total}")



seen = dict()
max_iter = 12_000
iter_to_positions = loop2(max_iter)
with open("day_14/trees_txt.txt","a") as file:
    for k in range(1, max_iter):
        GRID_TEST = np.array([["." for _ in range(GRID_SIZE_TEST[1])] for _ in range(GRID_SIZE_TEST[0])])
        positions = iter_to_positions[k]
        c = Counter(positions)
        for pos in c.keys():
            i, j = pos
            GRID_TEST[i][j] = c[pos]
        file.write(f"Iteration {k}\n")
        text = to_text(GRID_TEST)
        file.write(text)
        file.write("\n\n")
        if k % 1000 == 0:
            print(f"Done with iteration {k}")
        if text in seen.values():
            print(f"Cycle at iteration {k}")
            break
        seen[k] = text
        # print(f"Score at iteration {i} is {score}")
    file.close()


