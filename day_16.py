from typing import List, Tuple
from time import time as time
from collections import defaultdict
import heapq # a good datastructure for getting an element with lowest cost from a list
start = time()

# Two printing methods
def print_grid(grid):
    for row in grid:
        print("".join(row))

def print_distances_in_grid(grid, node_to_distance):
    str_grid = []
    for r, row in enumerate(grid):
        str_row = ""
        for c, val in enumerate(row):
            if val == "#":
                val = " ### "
            elif (r, c) not in node_to_distance.keys(): 
                val = f"{val:5}"
            else:
                val = f"{node_to_distance[(r, c)]:5}"
            str_row += val
        str_row += "\n"
        str_grid.append(str_row)
    for line in str_grid:
        print(line)

def print_unique_tilings(grid, tiles):
    copy_grid = [list(row) for row in grid]
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if (r, c) not in tiles: continue
            copy_grid[r][c] = "O"
    print_grid(copy_grid)



data = open("day_16/data_16.txt")
# Parsing the input and setting up some variables
grid = [list(row) for row in data.read().split("\n")]
END_NODE = (1, len(grid[0]) - 2)
START_NODE = (len(grid) - 2, 1)
START_DIR = (0, 1)
# A quick check 
assert ((grid[START_NODE[0]][START_NODE[1]] == "S") and (grid[END_NODE[0]][END_NODE[1]] == "E"))

def get_possible_directions(dr, dc: Tuple[int, int]) -> Tuple[int, int]:
    """
        Ensures that you cannot move back from where you came from.
    """
    directions = [(0,1), (1,0), (0,-1), (-1,0)] # right, down, up, left
    # We want to return all the directions, except the opposite direction
    assert (dr, dc) in directions
    directions.remove((-dr, -dc))
    return directions


def part1():
    # Part 1
    # In the normal Dijkstra algorithm, just the position is the state.
    # Now, the position AND the direction are part of the state.
    # cost, start node, start dir
    queue = [(0, *START_NODE, *START_DIR)]
    seen = set()
    done = False
    while queue:
        # print(f"\nQueue {queue}")
        cost, r, c, dr, dc = heapq.heappop(queue)
        if (r, c) == END_NODE:
            print(f"Found the shortest path {cost}")
            done = True
            break
        seen.add((r, c, dr, dc))
        for dir in get_possible_directions(dr, dc):
            cdr, cdc = dir
            nr, nc = r + cdr, c + cdc
            # If we move into a wall, skip
            if grid[nr][nc] == "#": continue
            # If we have seen this option before, skip
            if (nr, nc, cdr, cdc) in seen: continue
            # If we cannot move in the current direction, change direction
            # and add this element in the queue. Add 1000 to the cost
            # to get to this state.
            if (dr, dc) != dir:
                heapq.heappush(queue, (cost + 1000, r, c, *dir))
            else:
                heapq.heappush(queue, (cost + 1, nr, nc, *dir))
    if not done:
        assert False


# part1() # about 2.5 seconds, which is quite slow...

# For part 2, we do need to modify our code a little.
# It is now important that we know from where we came.

def part2():
    # Part 2 (solves part 1 too.)
    # Differences: 
    #   - Don't break anymore when the end state is reached
    #   - Implement something to keep track of the possible paths 
    #     we do this by keeping track from what positions we came
    #     from. Then we can construct all the paths when we backtrack
    #     from the END_NODE. We will store the previous node in the heapqueue
    #     so that we can build a path starting from the possible end states.

    # A crucial observation to this is that once a state is processed, it is surely the 
    # cheapest option to get to that state!! Suppose this is not the case, then we would 
    # have e.g. (r, c, dr, dc) = 1000, and then if at some point later we have (r, c, dr, dc) = 500
    # then the heappop would not have selected the lowest cost out of the queue! 

    state_to_cost = defaultdict(lambda: float("inf"))
    came_from = {}
    queue = [(0, *START_NODE, *START_DIR, None, None, None, None)]
    done = False
    best_cost = float('inf')
    end_states = set()
    counter = 0
    while queue:
        # print(f"\nQueue {queue}")
        cost, r, c, dr, dc, prev_r, prev_c, prev_dr, prev_dc = heapq.heappop(queue)
        if (r, c) == END_NODE:
            counter += 1
            if cost > best_cost: 
                done = True
                print(f"We have {counter - 1} many optimal paths")
                break
            best_cost = cost
            end_states.add((r, c, dr, dc))
        # If at some point we process another node that has a cost 
        # in the same state, we check if it is higher than the FIRST TIME (lowest cost)
        # we processed it. If this is the case, we do not continue, we can cut off this branch
        # Note that if the same state doesn't get added in between, the cost we get 
        # from the heappop wil be equal to state_to_cost[(r, c, dr, dc)]. 
        # This condition will not make us continue, we will in fact 
        # explore this option also.
        if cost > state_to_cost[(r, c, dr, dc)]: continue
        state_to_cost[(r, c, dr, dc)] = cost


        # Make sure to add where we came from
        if (r, c, dr, dc) not in came_from.keys():
            came_from[(r, c, dr, dc)] = set()
        came_from[(r, c, dr, dc)].add((prev_r, prev_c, prev_dr, prev_dc))


        for dir in get_possible_directions(dr, dc):
            cdr, cdc = dir
            nr, nc = r + cdr, c + cdc
            # If we move into a wall, skip
            if grid[nr][nc] == "#": continue
            # Check if we are moving into the same direction.
            # if not, we stay at our current position, and we 
            # add a cost of 1000. If we can move into the 
            # current direction, just add 1
            if (dr, dc) != dir:
                to_add = 1000
                nr, nc = r, c
            else:
                to_add = 1
            # Check what (so far) the cheapest way is to get here. (defaults to inf)
            cheapest_cost_to_get_here = state_to_cost[(nr, nc, *dir)]
            # If we found another way to get to the same state, but the cost is higher, we do not 
            # want to process this option --> continue
            if cost + to_add > cheapest_cost_to_get_here: continue

            # Whereas before, after seeing it once, we could skip an option, now we do have to check that we
            # actually get the lowest cost.
            # If we have seen this option before, skip
            # if (nr, nc, cdr, cdc) in seen: continue

            # Add the element to the queue.
            heapq.heappush(queue, (cost + to_add, nr, nc, *dir, r, c, dr, dc))
                
    if not done:
        assert False

    # Read out the back_track dictionary 'came_from'
    points = {END_NODE, START_NODE}
    backtrack_queue = list(end_states)

    while backtrack_queue:
        cur_point = backtrack_queue.pop(0)
        if cur_point == (*START_NODE, *START_DIR): continue
        for p in came_from[cur_point]:
            r, c, _, _ = p
            points.add((r, c))
            backtrack_queue.append(p)

    print(f"Number of unique tiles {len(points)}")
    print(f"Best cost {best_cost}")

    # print_unique_tilings(grid, points)


part2()
print(f"Time {time() - start:.5f}")

