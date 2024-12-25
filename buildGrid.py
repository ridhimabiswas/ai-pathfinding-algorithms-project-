from matplotlib import pyplot as plt
from matplotlib.pyplot import gcf, draw, pause
from matplotlib import colors as mcolors
import numpy as np
import random
import createMaze

class MazeGrid():

    def __init__(self):
        pass

    def create_new_maze(self):
        self.grid = createMaze.MazeGenerator(0, 0, 101, 101).Grid

    def display_maze(self):
        self.grid[0][0] = -1
        self.grid[-1][-1] = -1
        plt.figure(figsize=(8, 8))
        cmap = mcolors.ListedColormap(["red", "white", "black"])
        self.fig_plot = plt.imshow(self.grid, cmap=cmap)
        ax = plt.gca()

        ax.set_xticks(np.arange(-.5, 101, 1), minor=True)
        ax.set_yticks(np.arange(-.5, 101, 1), minor=True)

        ax.grid(which='minor', color='black', linestyle='-', linewidth=1)

        plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        plt.show()

    def highlight_path(self, path_coords):
        for row, col in path_coords:
            self.grid[col][row] = 2
        self.grid[0][0] = -1
        self.grid[-1][-1] = -1

        plt.figure(figsize=(8, 8))
        cmap = mcolors.ListedColormap(["#2bf016", "gray", "white", "#008080"])
        self.fig_plot = plt.imshow(self.grid, cmap=cmap)
        ax = plt.gca()

        ax.set_xticks(np.arange(-.5, 101, 1), minor=True)
        ax.set_yticks(np.arange(-.5, 101, 1), minor=True)

        ax.grid(which='minor', color='black', linestyle='-', linewidth=1)

        plt.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        plt.show()
