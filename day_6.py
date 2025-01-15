from typing import List, Tuple, Set
import numpy as np

from dataclasses import dataclass, field
from time import time as time

class Grid:

    def __init__(self, data):    
        self.data = data
        self.grid = []
        # Parse the grid
        self.parse_grid()
        # Set the current position and direction
        self.current_position: Tuple[int, int] = None
        self.find_current_position()
        self.current_direction: str = None
        self.find_current_direction()
        # Initalize the visited states with the current position
        self.pos_dir = set()
        self.add_to_pos_dir()
        self.visited_states: List[Tuple[int, int]] = [self.current_position]
        self.escaped = False
        print(f"Succesfull init...\n")


    def add_to_pos_dir(self):
        self.pos_dir.add((self.current_position, str(self.current_direction)))

    def get_visited_states(self) -> List[Tuple[int, int]]:
        return self.visited_states

    def parse_grid(self):
        if self.find_current_position() is not None:
            raise ValueError("You shouldn't parse the grid more than once")
        for line in self.data:
            els = []
            for el in line.strip():
                els.append(el)
            self.grid.append(els)
    
        self.grid = np.array(self.grid)
        # print(f"The parsed grid is: \n{self.grid}\n--")

    def __to_string__(self):
        print(self.grid)

    def find_current_position(self) -> Tuple[int, int]:
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] != "." and self.grid[i][j] != "#":
                    self.current_position = (i, j)
                     
            
    def find_current_direction(self) -> str:
        self.current_direction = self.grid[self.current_position[0]][self.current_position[1]]
        assert self.current_direction in ["^", "v", ">", "<"]

    def is_possible(self) -> bool:
        try:
            if self.current_direction == "^":
                if self.current_position[0] - 1 < 0:
                    raise IndexError("We escaped the grid!")
                if self.grid[self.current_position[0] - 1][self.current_position[1]] != "#": 
                    return True
                else:
                    return False
            elif self.current_direction == "v":
                if self.grid[self.current_position[0] + 1][self.current_position[1]] != "#":
                    return True
                else:
                    return False
            elif self.current_direction == ">":
                if self.grid[self.current_position[0]][self.current_position[1] + 1] != "#":
                    return True
                else:
                    return False
            elif self.current_direction == "<":
                if self.current_position[1] - 1 < 0:
                    raise IndexError("We escaped the grid!")
                if self.grid[self.current_position[0]][self.current_position[1] - 1] != "#":
                    return True
                else:
                    return False
                
        except IndexError:
            # print("We escaped the grid!")
            self.escaped = True


    def switch_directions(self) -> None:
        if self.current_direction == "^":
            self.grid[self.current_position[0]][self.current_position[1]] = ">"
        elif self.current_direction == ">":
            self.grid[self.current_position[0]][self.current_position[1]] = "v"
        elif self.current_direction == "v":
            self.grid[self.current_position[0]][self.current_position[1]] = "<"
        elif self.current_direction == "<":
            self.grid[self.current_position[0]][self.current_position[1]] = "^"
        
    def move(self) -> np.array:
        if self.current_direction == "^":
            self.grid[self.current_position[0]][self.current_position[1]] = "."
            self.grid[self.current_position[0] - 1][self.current_position[1]] = "^"
            self.current_position = (self.current_position[0] - 1, self.current_position[1])

        elif self.current_direction == "v":
            self.grid[self.current_position[0]][self.current_position[1]] = "."
            self.grid[self.current_position[0] + 1][self.current_position[1]] = "v"
            self.current_position = (self.current_position[0] + 1, self.current_position[1])

        elif self.current_direction == ">":
            self.grid[self.current_position[0]][self.current_position[1]] = "."
            self.grid[self.current_position[0]][self.current_position[1] + 1] = ">"
            self.current_position = (self.current_position[0], self.current_position[1] + 1)

        elif self.current_direction == "<":
            self.grid[self.current_position[0]][self.current_position[1]] = "."
            self.grid[self.current_position[0]][self.current_position[1] - 1] = "<"
            self.current_position = (self.current_position[0], self.current_position[1] - 1)

        # Add the new state that we moved to to the visited states
        self.visited_states.append(self.current_position)
        #Check if we are in a loop
        # print(f"current position {self.current_position}, current direction {self.current_direction}")
        # print(f"pos_dir {self.pos_dir}\n")
        if (self.current_position, str(self.current_direction)) in self.pos_dir:
            print(f"WE ARE IN A LOOP")
            self.escaped = False 
            self.loop = True
        self.add_to_pos_dir()



    def count_visited_states(self) -> int:
        return len(set(self.visited_states))

    def simulate(self) -> bool:
        # print(f"simulate with the grid:\n{self.grid}")
        # print(f"Starting simulation...\n")
        i = 0
        t0 = time()
        self.find_current_position()
        self.loop = False
        while not self.escaped and not self.loop:
            self.find_current_direction()
            # print("-----------")
            # print(self.grid)
            # print(f"Move possible {self.is_possible()}")
            if self.is_possible():
                self.move() 
            else:
                self.switch_directions()
            if i > 10000:
                print(f"Limit reached...\n")
                break
            i += 1
            # Add the new position to the set 

        # if self.escaped:
            # print(f"It took {time() - t0} seconds to escape...")
            # print(set(self.visited_states))
            # print(f"\n# Visited states {self.count_visited_states()}...")
            # Print the states we have visited
        
        return self.escaped


data = open("day_6/data_6.txt")

def parse_grid():
    data = open("day_6/data_6.txt")
    grid = []
    for line in data:
        els = []
        for el in line.strip():
            els.append(el)
        grid.append(els)
    return(np.array(grid))


grid = Grid(data=data)

# grid.simulate()

num_loops = 0
copy_grid = grid.grid[::]


# grid.grid[6][3] = "#"
# grid.simulate()


for i in range(copy_grid.shape[0]):
    for j in range(copy_grid.shape[1]):
        # if i != 6 or j != 3:
        #     continue
        if grid.grid[i][j] == ".":
            # print()
            # print(i, j)
            grid.grid[i][j] = "#"
            # print(f"we simulate")
            if not grid.simulate():
                # print(f"Loop found at {i, j}")
                num_loops += 1
            # Reset the grid
            grid.grid = parse_grid()
            grid.escaped = False   
            grid.loop = False 
            grid.pos_dir = set()

            

print(f"Number of loops: {num_loops}")

# do it like this: grid = np.array([list(i) for i in raw.split('\n')])