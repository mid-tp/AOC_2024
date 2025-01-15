from typing import List, Tuple
import numpy as np
data = open("day_10/data_10.txt")

from time import time as time
class Map:
    def __init__(self, data):
        self.data = data
        self.create_map()
        self.starting_points: List[Tuple[int, int]] = []
        self.find_starting_points()

    def create_map(self):
        self.map = []
        for line in data:
            els = []
            for i in line.strip():
                if i == ".":
                    i = -99
                else:
                    i = int(i)
                els.append(i)
            self.map.append(els)
        self.map = np.array(self.map)
        print(self.map)


    def find_starting_points(self) -> List[Tuple[int, int]]:
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                if self.map[i][j] == 0:
                    self.starting_points.append((i, j))

    def get_next_possible_steps(self, i, j) -> List[Tuple[int, int]]:
        """
            Check all directions with value increased by exactly 1
        """
        height = self.map[i][j]
        next_possible_steps = []
        # Up, Left, Down, Left
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for di, dj in directions:
            if i + di < 0 or j + dj < 0:
                continue
            try:
                if int(self.map[i + di][j + dj]) - int(height) == 1:
                    next_possible_steps.append((i + di, j + dj))
            except IndexError:
                pass
        return next_possible_steps
            
        
    def explore_starting_point(self, i, j) -> int:
        next_possible_steps = self.get_next_possible_steps(i, j)
        k = 0
        reachable_peaks = set()
        reachable_peaks = []
        while len(next_possible_steps) > 0:
            # print(f"\nThe next possible steps are:\n{next_possible_steps}")
            new_i, new_j = next_possible_steps.pop(0)
            if self.map[new_i][new_j] == 9:
                # print(f"Reached peak at {new_i, new_j}\n")
                # reachable_peaks.add((new_i, new_j))
                reachable_peaks.append((new_i, new_j))
            else:
                new_steps = self.get_next_possible_steps(new_i, new_j)
                next_possible_steps = new_steps + next_possible_steps
            if k > 20000:
                break
            k += 1

            # next_possible_steps = list(set(next_possible_steps))
        
        print(f"trailhead {i, j} has score {len(reachable_peaks)}")
        return len(reachable_peaks)

    def get_score(self):
        total = 0
        # self.starting_points = [(6, 0)]
        for starting_point in self.starting_points:
            print(f"\n\nChecking trailhead {starting_point}\n--------------------------------------")   
            total += self.explore_starting_point(*starting_point)
        print(f"Total score: {total}")


t0 = time()
map = Map(data)
print(map.starting_points)
map.get_score()

print(f"Execution time: {time() - t0}")