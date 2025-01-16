from typing import List, Tuple
import numpy as np
from collections import Counter

# I should have build in quicker checks to see if the move is actually valid
# Now I spend way too much time writing ugly code to fix the issue. 
# Might refactor this later.



class Grid:
    def __init__(self, data: List[str], part2: bool = False) -> None:
        self.data = data
        self.part2 = part2
        self.create_grid()
        self.get_dir = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}
        if self.part2:
            self.create_grid_part_2()
            self.grid = self.grid2

        self.update_current_pos()
        self.check_only_one_robot()
    def create_grid(self) -> List[List[str]]:       
        data_read = self.data.read().split("\n\n")
        # Get the instructions
        instruction_list = data_read[-1].split("\n")
        self.instructions = ""
        for partial_instruction in instruction_list:
            self.instructions += partial_instruction
        # Parse the grid
        lines = data_read[0].split("\n")
        grid = []
        for line in lines:
            grid.append([char for char in line])
        grid = np.array(grid)
        self.grid = grid

    def create_grid_part_2(self) -> None:
        grid2 = []
        for i in range(self.grid.shape[0]):
            current_row = []
            for j in range(self.grid.shape[1]):
                char = str(self.grid[i][j])
                if char == "#":
                    current_row.append("#")
                    current_row.append("#")
                elif char == ".":
                    current_row.append(".")
                    current_row.append(".")
                elif char == "O":
                    current_row.append("[")
                    current_row.append("]")
                elif char == "@":
                    current_row.append("@")
                    current_row.append(".")
                else:
                    raise ValueError("The character is not recognized.")
            grid2.append(current_row)
        grid2 = np.array(grid2)
        self.grid2 = grid2
        
    def count_number_boxes(self):
        total = 0
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if str(self.grid[i][j]) == "[":
                    assert str(self.grid[i][j + 1]) == "]"
                    total += 1
        return total
    
    def count_number_walls(self):
        total = 0
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if str(self.grid[i][j]) == "#":
                    total += 1
        return total


    def check_only_one_robot(self):
        # Loop over the entire grid, if there are more than 1 robot, raise an error
        count = 0 
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if str(self.grid[i][j]) == "@":
                    count += 1
        if count > 1:
            raise ValueError("There are more than 1 robot in the grid.")

    def update_current_pos(self) -> None:
        # Get the current position
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i][j] == "@":
                    self.current_pos = (i, j)
        
    def print_grid(self) -> None:
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                print(self.grid[i][j], end="")
            print()
    
    def print_grid2(self) -> None:
        for i in range(len(self.grid2)):
            for j in range(len(self.grid2[i])):
                print(self.grid2[i][j], end="")
            print()


    def get_object_at_next_pos_dir(self, pos, dir):
        return str(self.grid[pos[0] + dir[0]][pos[1] + dir[1]])
        
    def move_to_free_spot(self, cur_pos: Tuple[int, int], dir: Tuple[int, int], char: str) -> None:
        assert ((char == "@") or (char =="O") or (char == "[") or (char == "]"))
        self.grid[cur_pos[0]][cur_pos[1]] = "."
        self.grid[cur_pos[0] + dir[0]][cur_pos[1] + dir[1]] = char
        # Update the current position if necessary 
        if char == "@":
            # print(f"We move the robot {cur_pos} with {dir}")
            self.current_pos = (cur_pos[0] + dir[0], cur_pos[1] + dir[1])


    def check_if_pushing_possible(self, dir):
        done = False
        cur_pos = self.current_pos
        positions = []
        while not done:
            next_pos = (cur_pos[0] + dir[0], cur_pos[1] + dir[1])
            object_at_next_pos = str(self.grid[next_pos[0]][next_pos[1]])
            if object_at_next_pos == "#":
                return []
            elif object_at_next_pos == "O":
                positions.append(next_pos)
            elif object_at_next_pos == ".":
                done = True
            # Swap the current and the next position
            cur_pos = next_pos
        # Then
        return positions
    

    def flatten_box_indices_list(self, list_box_indices: List[Tuple[Tuple[int, int], Tuple[int, int]]]) -> List[Tuple[int, int]]:
        flattened = []
        for box in list_box_indices:
            index1, index2 = box
            flattened.append(index1)
            flattened.append(index2)
        return flattened

    def get_index_of_pair(self, pos, char):
        if char == "[":
            other_index = (pos[0], pos[1] + 1)
            assert self.grid[other_index[0]][other_index[1]] == "]"
            return (pos[0], pos[1] + 1)
        elif char == "]":
            other_index = (pos[0], pos[1] - 1)
            assert self.grid[other_index[0]][other_index[1]] == "["
            return other_index
        else:
            raise ValueError("The character for the pair is invalid...")
        
    def get_box_indices(self, current_box_index: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        current_char = self.grid[current_box_index[0]][current_box_index[1]]
        assert current_char == "[" or current_char == "]"
        other_index_of_box = self.get_index_of_pair(current_box_index, current_char)
        if current_char == "[":
            
            return (current_box_index, other_index_of_box)
        elif current_char == "]":
            return (other_index_of_box, current_box_index)
        else:
            raise ValueError("Get box indices wrong box character...")

        
    def get_adjecent_boxes(self, box_indices: Tuple[Tuple[int, int], Tuple[int, int]], dir) -> List[Tuple[int, int]]:
        # We cannot go into our own box indices
        own_index1, own_index2 = box_indices
        own_indices = {own_index1, own_index2}
        # Loop over the indices, and move into the next direction
        # Check if the next position is a box, if so, check if we are already
        # on it and if not, get the box associated with it
        indices_adjacent_boxes = []
        added_already = set()
        for indices in own_indices:
            next_pos = (indices[0] + dir[0], indices[1] + dir[1])
            if next_pos in own_indices:
                continue
            object_at_next_pos = str(self.grid[next_pos[0]][next_pos[1]])
            if object_at_next_pos == "[" or object_at_next_pos == "]":
                adjacent_box = self.get_box_indices(next_pos)
                if adjacent_box in indices_adjacent_boxes:
                    continue
                indices_adjacent_boxes.append(adjacent_box)
        

        return indices_adjacent_boxes
    

    def get_objects_from_box_dir(self, box: Tuple[Tuple[int, int], Tuple[int, int]], dir: Tuple[int, int]) -> Tuple[str, str]:
        pos1, pos2 = box
        return (self.grid[pos1[0] + dir[0]][pos1[1] + dir[1]], self.grid[pos2[0] + dir[0]][pos2[1] + dir[1]])

    def check_if_pushing_possible2(self, dir):
        # Check that at least we call the function correctly
        assert ((self.grid[self.current_pos[0] + dir[0]][self.current_pos[1] + dir[1]] == "[") or (self.grid[self.current_pos[0] + dir[0]][self.current_pos[1] + dir[1]] == "]"))
        queue: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        positions: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        next_pos = (self.current_pos[0] + dir[0], self.current_pos[1] + dir[1])
        box_indices = self.get_box_indices(next_pos)
        queue.append(box_indices)
        positions.append(box_indices)
        seen = set()
        # print(f"Current position {self.current_pos}")
        while queue:
            # print(f"\n\nQueue: {queue}")
            curent_box = queue.pop(0)
            seen.add(curent_box)
            # print(f"Current box {curent_box}")
            surrounding_boxes = self.get_adjecent_boxes(curent_box, dir)
            # print(f"Surrounding boxes: {surrounding_boxes}")    
            if len(surrounding_boxes) > 0:
                # check the surrounding boxes. If one box is adjacent to a wall
                # we return an empty list.
                for box in surrounding_boxes:
                    if box in seen:
                        continue
                    # If any of the next boxes is already adjacent to a wall
                    # we make sure we don't move.
                    object1, object2 = self.get_objects_from_box_dir(box, dir)
                    # print(f"Surrounding objects of box {box} {object1}, {object2}")
                    if object1 == "#" or object2 == "#":
                        return []
                    queue.append(box)
                    positions.append(box)
            else:
                # If there are no surrounding boxes in the direction, we check if 
                # we are adjacent to a wall.
                object1, object2 = self.get_objects_from_box_dir(curent_box, dir)
                if object1 == "#" or object2 == "#":
                    return []
                # If either one or both of the objects are a dot, we can move
                # We do nothing, as we might need to check more options
        # print(f"Positions before returning {positions} {dir}")
        # Flatten positions here
        # print(f"Before flattening: {positions}")





        positions = self.flatten_box_indices_list(positions)
        positions = list(set(positions)) # make sure we don't have duplicates

        if dir == (0, -1):
            # Sort the list on increasing second position of the tuple
            positions = sorted(positions, key=lambda x: x[1])
        elif dir == (0, 1):
            # Going up, the list should be sorted where the
            positions = sorted(positions)[::-1]
            # print(f"Should be reversed: {positions}")
        elif dir == (-1, 0):
            # Going up, sorted defaults to the first position
            positions = sorted(positions)
        elif dir == (1, 0):
            positions = sorted(positions)[::-1]
        else:
            raise ValueError("Invalid direction...")
        

        # Do a hardcoded check that we surely cannot reach any wall
        for position in positions:
            object_at_next_pos = str(self.grid[position[0] + dir[0]][position[1] + dir[1]])
            if object_at_next_pos == "#":
                return []
        

        return positions




    def move_possible(self, move: Tuple[int, int]) -> bool:
        dir = self.get_dir[move]
        # Check if the move is possible
        object_at_next_pos = str(self.grid[self.current_pos[0] + dir[0]][self.current_pos[1] + dir[1]])
        # print(f"Object at next position: {object_at_next_pos} {move}") 
        # print(f"Current position: {self.current_pos}")  

        if self.part2:
            char_to_check1 = "["
            char_to_check2 = "]"
        else:
            char_to_check1 = "O"
            char_to_check2 = "O"
        if object_at_next_pos == "#":
            # If we'd move immediately into a wall, we do not move
            return 
        elif object_at_next_pos == ".":
            # We go to a free spot, do that immediately
            # print(f"We make the move\n{move}")
            self.move_to_free_spot(self.current_pos, dir, "@")
        elif object_at_next_pos == char_to_check1 or object_at_next_pos == char_to_check2:
            # We push a box, check if we can push it.
            if not self.part2:
                positions = self.check_if_pushing_possible(dir)[::-1] # reverse the list
            else:
                positions = self.check_if_pushing_possible2(dir)
            
            if positions:
                # print(f"We make the move\n{move}")
                # Move all the elements by the current move
                num_boxes_to_push = len(positions) / 2
                num_boxes_to_push = 0
                if num_boxes_to_push > 5:
                    print(f"Number of boxes to push: {num_boxes_to_push}")
                    print(f"\nBefore making the move: {move} {self.current_pos}")
                    self.print_grid()
                for position in positions:
                    self.move_to_free_spot(position, dir, self.grid[position[0]][position[1]])
                # In the end, move ourselves
                self.move_to_free_spot(self.current_pos, dir, "@")
                if num_boxes_to_push > 5:
                    print(f"\nAfter making the move: {move} {self.current_pos}")
                    self.print_grid()
                    print(f"********************************************************************************************************************")

            else:
                # print(f"We cannot make the move {move} {self.current_pos}")
                # self.print_grid()
                pass
                # print(f"The boxes cannot be pushed.")


    def simulate(self):
        initial_num_boxes = self.count_number_boxes()
        initial_num_walls = self.count_number_walls()
        for i, move in enumerate(self.instructions):
            # print()
            self.move_possible(move)


            ## DEBUG ##
            # self.check_only_one_robot()
            # print(f"\nMaking the move: {move} (move #{i + 1})")
            # print(f"@ {self.current_pos}")
            # self.print_grid()

            # if initial_num_walls != self.count_number_walls():
            #     print(f"Initial number of walls {initial_num_walls}")
            #     print(f"Now {self.count_number_walls()}")
            #     raise ValueError("The number of walls has changed.")
            # get the new amount of number of boxes
            # if self.count_number_boxes() != initial_num_boxes:
            #     raise ValueError("The number of boxes has changed!")
            # if i > 1290:
            #     print(f"i loop")
            #     break
        if self.count_number_boxes() != initial_num_boxes:
            raise ValueError("The number of boxes has changed!")

    def calculate_GPS(self) -> int:
        # 100 * the distance from the top edge, so 100 times the i
        # and add the j component.
        print(f"\nFinal grid")
        self.print_grid()
        total = 0
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                char = str(self.grid[i][j])
                if char == "O" or char == "[":
                    total += 100 * i + j
        print(f"\nGPS score is: {total}")
        return total



grid = Grid(data =  open("day_15/data_15.txt"), part2=True)
print("Initial grid:")
grid.print_grid2()
grid.simulate()
grid.calculate_GPS()

# 1360257 is incorrect
