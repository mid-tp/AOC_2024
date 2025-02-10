from typing import List
import numpy as np
data = open("day_18/data_18.txt")




# print(GRID)

# Now do some sort of BFS, or Dijkstra type stuff.


directions = [(0,1), (1,0), (0,-1), (-1,0)] # right, down, up, left
def solution_from_bytes(GRID: np.array) -> int:
    start_node = (0,0)
    end_node = (GRID.shape[0] - 1, GRID.shape[1] - 1)
    node_to_distance = {start_node: 0}
    # assuming there is always a path possible
    queue = [start_node]
    while queue:
        node = queue.pop(0)
        i,j = node
        # print(node)
        for dir in directions:
            new_coords = (i + dir[0], j + dir[1])
            if new_coords[0] < 0 or new_coords[0] >= GRID_SIZE or new_coords[1] < 0 or new_coords[1] >= GRID_SIZE:
                continue
            # Check if we are not going out of bounds
            if GRID[new_coords[0], new_coords[1]] != "#":
                # This means we can reach this node
                # Check if we have already visited this node
                # Check if we have visited this node, if not, add it to the queue
                if new_coords not in node_to_distance.keys():
                    node_to_distance[new_coords] = node_to_distance[node] + 1
                    queue.append(new_coords)
                else:
                    # We have visited this node, we should check which path has the shortest distance
                    old_dist = node_to_distance[new_coords]
                    new_distance = node_to_distance[node] + 1
                    if new_distance < old_dist:
                        node_to_distance[new_coords] = new_distance

    if end_node in node_to_distance.keys():
        return node_to_distance[end_node]
    else:
        return -1



# Part 1
# First on the example
# grid size, 6x6

# initialize a grid with dots, then add # where
# we find the coordinates.
GRID_SIZE = 71
GRID = np.array([["." for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)])

for line in data:
    i, j = line.strip().split(",")
    # print(i, j)
    GRID[int(j), int(i)] = "#"
    # Check if there is a path to the end
    if solution_from_bytes(GRID) == -1:
        print(f"{i},{j}")
        print("There is no path")
        break



