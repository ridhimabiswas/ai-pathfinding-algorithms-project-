import random
import math

class MazeGenerator(object):

    def __init__(self, x_start, y_start, width=10, height=10):
        self.maze_grid = [[0 for _ in range(width)] for _ in range(height)]
        self.maze_grid[y_start][x_start] = 1
        self.frontier_cells = []
        self.width = width
        self.height = height

        self.update_frontier(x_start, y_start)
        while len(self.frontier_cells) > 0:
            self.expand_maze()
        
        self.add_loops(math.floor(math.sqrt(width * height) - 1 / 2))

    def set_cell_value(self, x, y, value):
        self.maze_grid[y][x] = value

    def get_cell_value(self, x, y):
        return self.maze_grid[y][x]

    def update_frontier(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            if 0 <= x - 2 < self.width and self.maze_grid[y][x - 2] != 1:
                if [x - 2, y] not in self.frontier_cells:
                    self.frontier_cells.append([x - 2, y])

            if 0 <= x + 2 < self.width and self.maze_grid[y][x + 2] != 1:
                if [x + 2, y] not in self.frontier_cells:
                    self.frontier_cells.append([x + 2, y])

            if 0 <= y - 2 < self.height and self.maze_grid[y - 2][x] != 1:
                if [x, y - 2] not in self.frontier_cells:
                    self.frontier_cells.append([x, y - 2])

            if 0 <= y + 2 < self.height and self.maze_grid[y + 2][x] != 1:
                if [x, y + 2] not in self.frontier_cells:
                    self.frontier_cells.append([x, y + 2])

    def find_neighbors(self, x, y):
        neighbors = []
        if 0 <= x < self.width and 0 <= y < self.height:
            if x - 2 >= 0 and self.maze_grid[y][x - 2] == 1:
                neighbors.append([x - 2, y])
            if x + 2 < self.width and self.maze_grid[y][x + 2] == 1:
                neighbors.append([x + 2, y])
            if y - 2 >= 0 and self.maze_grid[y - 2][x] == 1:
                neighbors.append([x, y - 2])
            if y + 2 < self.height and self.maze_grid[y + 2][x] == 1:
                neighbors.append([x, y + 2])
        return neighbors

    def direct_neighbors(self, x, y):
        adj_neighbors = []
        if 0 <= x < len(self.maze_grid) and 0 <= y < len(self.maze_grid):
            if x - 1 >= 0 and self.maze_grid[y][x - 1] == 1:
                adj_neighbors.append([x - 1, y])
            if x + 1 < len(self.maze_grid) and self.maze_grid[y][x + 1] == 1:
                adj_neighbors.append([x + 1, y])
            if y - 1 >= 0 and self.maze_grid[y - 1][x] == 1:
                adj_neighbors.append([x, y - 1])
            if y + 1 < len(self.maze_grid) and self.maze_grid[y + 1][x] == 1:
                adj_neighbors.append([x, y + 1])
        return adj_neighbors

    def expand_maze(self):
        frontier_idx = random.randint(0, len(self.frontier_cells) - 1)
        chosen_cell = self.frontier_cells[frontier_idx]
        neighbors = self.find_neighbors(chosen_cell[0], chosen_cell[1])
        selected_neighbor_idx = random.randint(0, len(neighbors) - 1)

        middle = self.find_middle(chosen_cell, neighbors[selected_neighbor_idx])
        mid_x, mid_y = middle[0], middle[1]

        self.maze_grid[chosen_cell[1]][chosen_cell[0]] = 1
        self.maze_grid[mid_y][mid_x] = 1

        self.frontier_cells.remove(chosen_cell)
        self.update_frontier(chosen_cell[0], chosen_cell[1])

    def add_loops(self, loop_count):
        for _ in range(loop_count):
            # Select a random point and one of its neighbors
            point1 = [round(random.randint(0, self.width - 1) / 2) * 2, round(random.randint(0, self.height - 1) / 2) * 2]
            point2 = random.choice(self.find_neighbors(point1[0], point1[1]))

            # Re-select points if they are already linked
            while self.maze_grid[self.find_middle(point1, point2)[1]][self.find_middle(point1, point2)[0]] == 1:
                point1 = [round(random.randint(0, self.width - 1) / 2) * 2, round(random.randint(0, self.height - 1) / 2) * 2]
                point2 = random.choice(self.find_neighbors(point1[0], point1[1]))
            self.maze_grid[self.find_middle(point1, point2)[1]][self.find_middle(point1, point2)[0]] = 1

    def find_middle(self, p1, p2):
        mid_x = mid_y = 0
        # X coordinates are equal
        if p1[0] == p2[0]:
            mid_x = p1[0]
            # Calculate middle Y
            if p1[1] > p2[1]:
                mid_y = p2[1] + 1
            else:
                mid_y = p1[1] + 1
        # Y coordinates are equal
        elif p1[1] == p2[1]:
            mid_y = p1[1]
            # Calculate middle X
            if p1[0] > p2[0]:
                mid_x = p2[0] + 1
            else:
                mid_x = p1[0] + 1

        return [mid_x, mid_y]
    
    @property
    def Grid(self):
        return self.maze_grid

    def display_grid(self):
        for row in self.maze_grid:
            for cell in row:
                if cell == 0:
                    print(" ", end=" ")
                elif cell == 1:
                    print("\033[1;32;40m\u25A0\033[1;30;40m", end=" ")
                elif cell == 2:
                    print("\033[1;34;40m\u25A0\033[1;30;40m", end=" ")
                elif cell == 3:
                    print("\033[1;31;40m\u25A0\033[1;30;40m", end=" ")
            print("\n", end="")

