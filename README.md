# AOC_2024
My code for Advent of Code 2024

Things I would do differently the next years:
- Make sure that if you're changing values of a grid, build in some checks for elements that shouldn't be changed. In many puzzles, you need to make a move or "move objects around" in the grid. For example, count the number of elements that should stay the same before and after the simulation, and check if these values are the same. Also, create a manual check if a move is possible. (These tips definitely would have saved me quite some time in e.g. day 15 p2 :) )
- When parsing data into a grid, make use of map() and list(), this makes your easier to write, while mainting readability

Some tips for next years:
- Practice on some of the recursion problems. Rewrite problems after seeing a smarter/easier solution method for days which were difficult at first.
