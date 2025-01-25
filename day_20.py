from typing import List
from aoc_helpers.grid_dijkstra import *
from collections import Counter
from time import time as time
data = open("day_20/data_20.txt")

grid = [list(row) for row in data.read().split("\n")]

# We can loop over each row, and get consecutive elements.
# If one of them is a . and the other a wall, we might create a shortcut.
# We will store the cheats by the indices.
# The first index should always be a wall #

def highlight_cheat(grid: List[List[str]], cheat: Tuple[int, int, int, int], num: str) -> None:
    r, c, rr, cc = cheat
    grid[r][c] = "1"
    grid[rr][cc] = num
    print_grid(grid)


def part1(grid: List[List[str]], to_print: bool = False):
    # Make a copy of the grid.
    copy_grid = [list(row) for row in grid]
    distances = dijkstra(grid, to_print=to_print)
    cheat_to_score = {}
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            # Skip if we are going out of bounds
            if (c == 0) or (c == len(row) - 1): continue
            if (r == 0) or (r == len(grid) - 1): continue
            if copy_grid[r][c] != "#": continue
            
            # Check for horizontal cheat
            if copy_grid[r][c + 1] != "#" and copy_grid[r][c - 1] != "#":
                cheat_to_score[(r, c)] = abs(distances[(r, c + 1)] - distances[(r, c - 1)]) - 2

            if (r, c) in cheat_to_score.keys(): continue
            # Check for vertical cheat
            if copy_grid[r + 1][c] != "#" and copy_grid[r - 1][c] != "#":
                cheat_to_score[(r, c)] = abs(distances[(r + 1, c)] - distances[(r - 1, c)]) - 2

    c = Counter(cheat_to_score.values())
    t = 0
    for key in sorted(c.keys()):
        # print(f"{c[key]} cheat(s) save {key} seconds")
        if key >= 100:
            t += c[key]

    print(f"({t})")


def throw_away_states(grid: List[List[str]], states: List[Tuple[int, int]]):
    """
        Make sure we do not move out of bounds
    """
    correct_states = []
    for state in states:
        r, c = state
        correct_states.append(state)
    return correct_states

def generate_possible_nodes_from_distance(grid: List[List[str]], cur_node: List[Tuple[int, int]], dist: int):
    possible_options = []
    r, c = cur_node
    for dr in range(-dist, dist + 1):
        for dc in range(-dist, dist + 1):
            nr, nc = r + dr, c + dc
            if abs(dr) + abs(dc) != dist: continue
            if nr <= 0 or nc <= 0 or nr >= len(grid) - 1 or nc >= len(grid[0]) - 1: continue
            if grid[nr][nc] == "#": continue
            possible_options.append((nr, nc))
    return throw_away_states(grid, possible_options)


def part2(grid, num_steps: int = 2, to_print: bool = False):
    """
        Now we have to take into account the fact that we can reach anywhere in these 20 seconds

        I guess you take the minimum value you could reach in 20 steps, and then just take the difference
        from that point. And take the mimimum value from there.
    """
    copy_grid = [list(row) for row in grid]
    distances = dijkstra(grid, to_print=to_print)
    cheat_to_score = {}
    # For any node, that is a ".", check all the possible nodes where you can end up in 'num_steps' steps.
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if r == 0 or c == 0 or r >= len(grid) - 1 or c >= len(grid[0]) - 1: continue
            if (r, c) not in distances.keys(): continue
            if val == "E": continue

            # Check all the positions that we can visit from the current state, in 'num_steps' steps.
            able_to_visit = generate_possible_nodes_from_distance(grid, (r, c), num_steps)

            # We want to add all the cheats that reduce the cost
            for node in able_to_visit:
                rr, cc = node
                if copy_grid[rr][cc] == "#": continue
                if node not in distances.keys(): continue
                new_cost = distances[node] - distances[(r, c)] - num_steps
                if new_cost <= 0: continue
                cheat_to_score[r, c, *node] = new_cost

    return cheat_to_score

def solve2(grid, num_steps: int = 20):
    seconds_saved_to_count = defaultdict(lambda: 0)
    for i in range(2, num_steps + 1):
        # print(f"\nTaking {i} steps...")
        num_to_score = part2(grid, num_steps=i)
        for seconds_saved in num_to_score.values():
            if seconds_saved < 50: continue
            seconds_saved_to_count[seconds_saved] += 1

    # for key in sorted(seconds_saved_to_count.keys()):
    #     print(f"There are {seconds_saved_to_count[key]:4} cheat(s) that save {key:3} picoseconds...")
    l = sum([seconds_saved_to_count[key] for key in seconds_saved_to_count.keys() if key >= 100])
    print(l)

start = time()
# part1(grid, to_print = True)
# part2(grid, to_print=True, num_steps=20)
solve2(grid, num_steps = 20)


print(f"Time {time() - start:.4f}")






# 1020507





# 1235210
# 6091089 too high
# 3322709 too high
# 900469 not the right answer... ?

# Need to check what is going on here. Check the examples once more.

# Perhaps it is the case that a cheat should START in a wall?