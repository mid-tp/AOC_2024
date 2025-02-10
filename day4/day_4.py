from typing import List
import numpy as np 
from scipy.ndimage import rotate

data = open("day_4/data_4.txt")


def check_horizontal(i: int, j: int, grid: np.array) -> int:
    count = 0
    try:
        if grid[i][j] == "X" and grid[i][j + 1] == "M" and grid[i][j + 2] == "A" and grid[i][j + 3] == "S":
            count += 1     
    except IndexError as e:
        pass
    try:
        if j - 3 >= 0 and grid[i][j] == "X" and grid[i][j - 1] == "M" and grid[i][j - 2] == "A" and grid[i][j - 3] == "S":
            count += 1
    except IndexError as e:
        pass
    return count


def check_vertical(i: int, j: int, grid: np.array) -> int:
    count = 0
    try:
        if grid[i][j] == "X" and grid[i + 1][j] == "M" and grid[i + 2][j] == "A" and grid[i + 3][j] == "S":
            count += 1
    except IndexError as e:
        pass
    try:
        if i - 3 >= 0 and grid[i][j] == "X" and grid[i - 1][j] == "M" and grid[i - 2][j] == "A" and grid[i - 3][j] == "S":
            count += 1
    except IndexError as e:
        pass
    return count


def check_diagonals(i: int, j: int, grid: np.array) -> int:
    count = 0
    try:
        if grid[i][j] == "X" and grid[i + 1][j + 1] == "M" and grid[i + 2][j + 2] == "A" and grid[i + 3][j + 3] == "S":
            print(f"FOUND DIAGONAL AT ({i},{j}) 1")
            count += 1
    except IndexError as e:
        pass
    try:
        if j - 3 >= 0 and grid[i][j] == "X" and grid[i + 1][j - 1] == "M" and grid[i + 2][j - 2] == "A" and grid[i + 3][j - 3] == "S":
            print(f"FOUND DIAGONAL AT ({i},{j}) 2")
            count += 1
    except IndexError as e:
        pass
    try:
        if i - 3 >= 0 and grid[i][j] == "X" and grid[i - 1][j + 1] == "M" and grid[i - 2][j + 2] == "A" and grid[i - 3][j + 3] == "S":
            print(f"FOUND DIAGONAL AT ({i},{j}) 3")
            count += 1
    except IndexError as e:
        pass
    try: 
        if j - 3 >= 0 and i - 3 >= 0 and  grid[i][j] == "X" and grid[i - 1][j - 1] == "M" and grid[i - 2][j - 2] == "A" and grid[i - 3][j - 3] == "S":
            print(f"FOUND DIAGONAL AT ({i},{j}) 4")
            count += 1
    except IndexError as e:
        pass
    return count


def find_x_mas(i: int, j: int, grid) -> bool:
    # Check if there is 
    if grid[i][j] != "A" or i + 1 >= grid.shape[0] or j + 1 >= grid.shape[1] or i - 1 < 0 or j - 1 < 0:
        return False
    if grid[i - 1][j - 1] == "M" and grid[i + 1][j + 1] == "S" and grid[i-1][j + 1] == "M" and grid[i + 1][j - 1]== "S":
        print(f"1 ({i},{j})")
        return True
    if grid[i - 1][j - 1] == "M" and grid[i + 1][j + 1] == "S" and grid[i-1][j + 1] == "S" and grid[i + 1][j - 1]== "M":
        print(f"2 ({i},{j})")
        return True
    if grid[i - 1][j - 1] == "S" and grid[i + 1][j + 1] == "M" and grid[i-1][j + 1] == "S" and grid[i + 1][j - 1]== "M":
        print(f"3 ({i},{j})")
        return True
    if grid[i - 1][j - 1] == "S" and grid[i + 1][j + 1] == "M" and grid[i-1][j + 1] == "M" and grid[i + 1][j - 1]== "S":
        print(f"4 ({i},{j})")
        return True
    
    return False

grid = []
for line in data:
    temp = []
    for el in line.strip():
        temp.append(el)
    grid.append(temp)

grid = np.array(grid)
# print(grid)
# print(find_x_mas(7, 1, grid))
# i = 7
# j = 1
# print(f"{grid[i - 1][j - 1]}\n {grid[i + 1][j + 1]}\n {grid[i-1][j + 1]}\n {grid[i - 1][j - 1]}")
# print(grid[6][0])
      
print(grid[4][2])

def check_grid(grid: np.array,two = False, hor = True, ver = True, diag = True) -> int:
    total = 0   
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if not two:
                if hor:
                    total += check_horizontal(i, j, grid)
                if ver:
                    total += check_vertical(i, j, grid)
                if diag:
                    total += check_diagonals(i, j, grid)
            else:
                if find_x_mas(i, j, grid):
                    total += 1
    return total


big_total = check_grid(grid, two = True)
print(big_total)


# doesn't give the right result for some reason, gives me 16 instead of 18


# def check_grid_diagonals(grid: np.array) -> int:
#     total = 0
#     for i in range(grid.shape[0]):
#         for j in range(grid.shape[1]):
#             if check_diagonals(i, j, grid):
#                 total += 1
#     return total

# def check_from_index(i: int, j: int, grid: np.array) -> bool:
#     try:
#         if grid[i][j] == "X" and grid[i][j + 1] == "M" and grid[i][j + 2] == "A" and grid[i][j + 3] == "S":
#             return True
#         else:
#             return False
            
#     except IndexError as e:
#         return False


# def check_diagonals(i: int, j: int, grid: np.array) -> bool:
#     try:
#         if grid[i][j] == "X" and grid[i + 1][j + 1] == "M" and grid[i + 2][j + 2] == "A" and grid[i + 3][j + 3] == "S":
#             return True
#     except IndexError as e:
#         pass
#     try:
#         if grid[i][j] == "X" and grid[i + 1][j - 1] == "M" and grid[i + 2][j - 2] == "A" and grid[i + 3][j - 3] == "S":
#             return True
#     except IndexError as e:
#         pass
        
#     try:
#         if grid[i][j] == "X" and grid[i - 1][j + 1] == "M" and grid[i - 2][j + 2] == "A" and grid[i - 3][j + 3] == "S":
#             return True
#     except IndexError as e:
#         pass

#     try: 
#         if grid[i][j] == "X" and grid[i - 1][j - 1] == "M" and grid[i - 2][j - 2] == "A" and grid[i - 3][j - 3] == "S":
#             return True
#     except IndexError as e:
#         pass
#     return False

# big_total = check_grid_diagonals(grid) 

# # Do all the possible combinations of the grid.
# for _ in range(2):
#     grid = np.flip(grid)
#     for _ in range(3):
#         grid = np.rot90(grid)
#         big_total += check_grid(grid) 

    
# print(big_total)
