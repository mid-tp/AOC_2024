# AOC_2024
My code for [Advent of Code 2024](https://adventofcode.com/2024)
(need to edit the table still!)

# Advent of Code 2024

My solutions to the Advent of Code puzzles for the 2024 edition, written in C#.

| AoC Puzzle | Part One | Part Two | Type | Difficulty |
|------------|---------|---------|------|------------|
| [Day 1: Historian Hysteria](day1/) | 1.1 ✅ | 1.2 ✅ | String Parsing | 🟢 Easy |
| [Day 2: Red-Nosed Reports](day2/) | 2.1 ✅ | 2.2 ✅ | Graph Traversal | 🟡 Medium |
| [Day 3: Mull It Over](day3/) | 3.1 ✅ | 3.2 ✅ | Dynamic Programming | 🔴 Hard |
| [Day 4: Ceres Search](day4/) | 4.1 ✅ | 4.2 ✅ | BFS/DFS | 🟡 Medium |
| [Day 5: Print Queue](day5/) | 5.1 ✅ | 5.2 ✅ | Priority Queue | 🟡 Medium |
| [Day 6: Guard Gallivant](day6/) | 6.1 ✅ | 6.2 ✅ | Simulation | 🔴 Hard |
| [Day 7: Bridge Repair](day7/) | 7.1 ✅ | 7.2 ✅ | Minimum Spanning Tree | 🔴 Hard |
| [Day 8: Resonant Collinearity](day8/) | 8.1 ✅ | 8.2 ✅ | Geometry | 🟡 Medium |
| [Day 9: Disk Fragmenter](day9/) | 9.1 ✅ | 9.2 ✅ | Bit Manipulation | 🟢 Easy |
| [Day 10: Hoof It](day10/) | 10.1 ✅ | 10.2 ✅ | Pathfinding | 🟡 Medium |
| [Day 11: Plutonian Pebbles](day11/) | 11.1 ✅ | 11.2 ✅ | Grid Search | 🔴 Hard |
| [Day 12: Garden Groups](day12/) | 12.1 ✅ | 12.2 ✅ | Union-Find | 🟡 Medium |
| [Day 13: Claw Contraption](day13/) | 13.1 ✅ | 13.2 ✅ | Stack Processing | 🟢 Easy |
| [Day 14: Restroom Redoubt](day14/) | 14.1 ✅ | 14.2 ✅ | Cellular Automata | 🔴 Hard |
| [Day 15: Warehouse Woes](day15/) | 15.1 ✅ | 15.2 ✅ | Sorting | 🟡 Medium |
| [Day 16: Reindeer Maze](day16/) | 16.1 ✅ | 16.2 ✅ | Pathfinding (A*) | 🔴 Hard |
| [Day 17: Chronospatial Computer](day17/) | 17.1 ✅ | 17.2 ❌ | Modular Arithmetic | 🟡 Medium |
| [Day 18: RAM Run](day18/) | 18.1 ✅ | 18.2 ✅ | Knapsack | 🔴 Hard |
| [Day 19: Linen Layout](day19/) | 19.1 ✅ | 19.2 ✅ | Greedy | 🟡 Medium |
| [Day 20: Race Condition](day20/) | 20.1 ✅ | 20.2 ✅ | Scheduling | 🔴 Hard |
| [Day 21: Keypad Conundrum](day21/) | 21.1 ✅ | 21.2 ❌ | State Machine | 🟡 Medium |
| [Day 22: Monkey Market](day22/) | 22.1 ✅ | 22.2 ✅ | Game Theory | 🔴 Hard |
| [Day 23: LAN Party](day23/) | 23.1 ✅ | 23.2 ✅ | Graph Coloring | 🟡 Medium |
| [Day 24: Crossed Wires](day24/) | 24.1 ✅ | 24.2 ❌ | Geometry | 🔴 Hard |
| [Day 25: Code Chronicle](day25/) | 25.1 ❌ | 25.2 ❌ | Data Structures | 🔴 Hard |

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Solved it myself |
| ❌ | Wasn't able to solve it myself |
| 🟢 | Easy |
| 🟡 | Medium |
| 🔴 | Hard |




Things I would do differently the next years:
- Make sure that if you're changing values of a grid, build in some checks for elements that shouldn't be changed. In many puzzles, you need to make a move or "move objects around" in the grid. For example, count the number of elements that should stay the same before and after the simulation, and check if these values are the same. Also, create a manual check if a move is possible. (These tips definitely would have saved me quite some time in e.g. day 15 p2 :) )
- When parsing data into a grid, make use of map() and list(), this makes your easier to write, while mainting readability

Some tips for next years:
- Practice on some of the recursion problems. Rewrite problems after seeing a smarter/easier solution method for days which were difficult at first.


