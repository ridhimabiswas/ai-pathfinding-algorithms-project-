import numpy
import time
import random
from statistics import mean, stdev
import sys
import math
import heapq
from heapq import heappush, heappop
import buildGrid
from buildGrid import MazeGrid as Grid
from minHeap import MinHeap


class Cell:
   def __init__(self, coordinate, parent=None, f_val=0, g_val=0, h_val=0):
       self.x = coordinate[0]
       self.y = coordinate[1]
       self.parent = parent
       self.f_value = f_val
       self.g_value = g_val
       self.h_value = h_val

cells_expanded = 0

def repeated_adaptive_AStar(initial, goal, grid):

   start = Cell(initial)
   end = Cell(goal)
   cells = {}
   cells[initial] = start 
   cells[goal] = end
   master_path = [initial]

   number_rows = len(grid)
   number_columns = len(grid[0])

   current = start

   neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]


   for neighbor in neighbors:
       if (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
           if grid[neighbor[1]][neighbor[0]] == 0:
               temp_cell = Cell(initial, current)
               temp_cell.g_value = float('inf')
               temp_cell.h_value = manhattanDistance(temp_cell, end)
               temp_cell.f_value = temp_cell.g_value
               cells[neighbor] = temp_cell

   while not(current.x == end.x and current.y == end.y):
      
       start_A_Star = current       
       cell = forward_adaptive_AStar(start_A_Star, end, cells, grid)
      
       path = []
       goal_g_value = end.g_value


       while not(cell.x == current.x and cell.y == current.y):
           path.append((cell.x, cell.y))
           cell.h_value = goal_g_value - cell.g_value
           cell = cell.parent

       cell.h_value = goal_g_value - cell.g_value


       #print(path)      
       for i in range(len(path)-1, -1, -1):
          
           next_x_coordinate = path[i][0]
           next_y_coordinate = path[i][1]
          
           if grid[next_y_coordinate][next_x_coordinate] == 0:
               cells[(next_x_coordinate, next_y_coordinate)].g_value = float('inf')
               cells[(next_x_coordinate, next_y_coordinate)].f_value = float('inf')
               break


           else:
               current = cells[(next_x_coordinate, next_y_coordinate)]
               master_path.append((next_x_coordinate, next_y_coordinate))

               neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]


               for neighbor in neighbors:
                   if (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
                       if grid[neighbor[1]][neighbor[0]] == 0:
                           temp_cell = Cell(initial, current)
                           temp_cell.g_value = float('inf')
                           temp_cell.h_value = manhattanDistance(temp_cell, end)
                           temp_cell.f_value = temp_cell.g_value
                           cells[neighbor] = temp_cell
              
   #print(master_path)
   return master_path

def repeated_forward_AStar(initial, goal, grid):

   start = Cell(initial)
   end = Cell(goal)
   cells = {}
   cells[initial] = start
   cells[goal] = end
   master_path = [initial]

   number_rows = len(grid)
   number_columns = len(grid[0])

   current = start

   neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]

   for neighbor in neighbors:
       if (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
           if grid[neighbor[1]][neighbor[0]] == 0:
               temp_cell = Cell(initial, current)
               temp_cell.g_value = float('inf')
               temp_cell.h_value = manhattanDistance(temp_cell, end)
               temp_cell.f_value = temp_cell.g_value
               cells[neighbor] = temp_cell

   while not(current.x == end.x and current.y == end.y):

       cell = forward_AStar(current, end, cells, grid)
       path = []
      
       while not(cell.x == current.x and cell.y == current.y):
           path.append((cell.x, cell.y))
           cell = cell.parent

       print(path)
       
       for i in range(len(path)-1, -1, -1):
          
           next_x_coordinate = path[i][0]
           next_y_coordinate = path[i][1]
          
           if grid[next_y_coordinate][next_x_coordinate] == 0:
               cells[(next_x_coordinate, next_y_coordinate)].g_value = float('inf')
               cells[(next_x_coordinate, next_y_coordinate)].f_value = float('inf')
               break


           else:
               current = cells[(next_x_coordinate, next_y_coordinate)]
               master_path.append((next_x_coordinate, next_y_coordinate))

               neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]


               for neighbor in neighbors:
                   if (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
                       if grid[neighbor[1]][neighbor[0]] == 0:
                           if (neighbor[0], neighbor[1]) in cells:
                               cells[neighbor].g_value = float('inf')
                               cells[neighbor].f_value = float('inf')
                           else:
                               temp_cell = Cell(initial, current)
                               temp_cell.g_value = float('inf')
                               temp_cell.h_value = manhattanDistance(temp_cell, end)
                               temp_cell.f_value = temp_cell.g_value
                               cells[neighbor] = temp_cell
          
   #print(master_path)
   return master_path

def forward_AStar(initial, goal, cells, grid):
  
   global cells_expanded
  
   #open_list = []
   initial.g_value = 0
   initial.f_value = initial.h_value


   number_rows = len(grid)
   number_columns = len(grid[0])
  
   #push(open_list, (initial.f_value, initial.g_value, random.random(), initial))
   open_list = MinHeap()
   open_list.push((initial.f_value, initial.g_value, random.random(), initial))
   closed_list = set()

   current = initial


   while open_list.length() > 0:
       #current_f_value, current_g_value, current_tiebreaker, current = pop(open_list)
       current_f_value, current_g_value, current_tiebreaker, current = open_list.pop()
      
       if (current.x, current.y) in closed_list:
           continue

       cells_expanded += 1
       closed_list.add((current.x, current.y))


       if current.x == goal.x and current.y == goal.y:
           return current

       neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]


       for neighbor in neighbors:
           if not (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
               continue
           if (neighbor[0], neighbor[1]) in closed_list:
               continue
           else:
               if neighbor not in cells:
                   temp_cell = Cell(neighbor, current)
                   cells[neighbor] = temp_cell
                   temp_g = current.g_value + 1
                   temp_h = manhattanDistance(temp_cell, goal)
                   temp_f = temp_g + temp_h
                   temp_cell.f_value = temp_f
                   temp_cell.g_value = temp_g
                   temp_cell.h_value = temp_h
              
                   #push(open_list, (temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
                   open_list.push((temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
                  
               else:
                   if cells[neighbor].g_value != float('inf'):
                       temp_cell = cells[neighbor]
                       temp_cell.parent = current
                       temp_g = current.g_value + 1
                       #temp_h = cells[neighbor].h_value
                       temp_h = manhattanDistance(temp_cell, goal)
                       temp_f = temp_g + temp_h
                       temp_cell.f_value = temp_f
                       temp_cell.g_value = temp_g
                       temp_cell.h_value = temp_h

                       #push(open_list, (temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
                       open_list.push((temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))

   return current

def forward_adaptive_AStar(initial, goal, cells, grid):
  
   global cells_expanded
  
   #open_list = [] # structure of each element should be as follows: (f-value, Cell object), heap
  
   initial.g_value = 0
   initial.f_value = initial.h_value


   number_rows = len(grid)
   number_columns = len(grid[0])
  
   #push(open_list, (initial.f_value, initial.g_value, random.random(), initial))
   open_list = MinHeap()
   open_list.push((initial.f_value, initial.g_value, random.random(), initial))
   closed_list = set()

   current = initial


   while open_list.length() > 0:
       #current_f_value, current_g_value, current_tiebreaker, current = pop(open_list)
       current_f_value, current_g_value, current_tiebreaker, current = open_list.pop()


      
       if (current.x, current.y) in closed_list:
           continue

       cells_expanded += 1
       closed_list.add((current.x, current.y))

       if current.x == goal.x and current.y == goal.y:
           return current

       neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]


       for neighbor in neighbors:
           if not (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
               continue
           if (neighbor[0], neighbor[1]) in closed_list:
               continue
           else:
               if neighbor not in cells:
                   temp_cell = Cell(neighbor, current)
                   cells[neighbor] = temp_cell
                   temp_g = current.g_value + 1
                   temp_h = manhattanDistance(temp_cell, goal)
                   temp_f = temp_g + temp_h
                   temp_cell.f_value = temp_f
                   temp_cell.g_value = temp_g
                   temp_cell.h_value = temp_h
              
                   #push(open_list, (temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
                   open_list.push((temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
                  
               else:
                   if cells[neighbor].g_value != float('inf'):
                       temp_cell = cells[neighbor]
                       temp_cell.parent = current
                       temp_g = current.g_value + 1
                       temp_h = cells[neighbor].h_value
                       #temp_h = manhattanDistance(temp_cell, goal)
                       temp_f = temp_g + temp_h
                       temp_cell.f_value = temp_f
                       temp_cell.g_value = temp_g
                       temp_cell.h_value = temp_h

                       #push(open_list, (temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
                       open_list.push((temp_cell.f_value, -temp_cell.g_value, random.random(), temp_cell))
   return current




def repeated_backward_AStar(initial, goal, grid):
   start = Cell(initial)
   end = Cell(goal)
   cells = {}
   cells[initial] = start
   cells[goal] = end
   master_path = [initial]


   number_rows = len(grid)
   number_columns = len(grid[0])


   current = start
   neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]


  
   for neighbor in neighbors:
       if (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
           if grid[neighbor[1]][neighbor[0]] == 0:
               temp_cell = Cell(initial, current)
               temp_cell.g_value = float('inf')
               temp_cell.h_value = manhattanDistance(temp_cell, start)
               temp_cell.f_value = temp_cell.g_value
               cells[neighbor] = temp_cell
  
   while not(current.x == end.x and current.y == end.y):

       start_A_Star = current       
       cell = repeated_backward_AStar(end, start_A_Star, cells, grid)
      
       path = []
       while not(cell.x == end.x and cell.y == end.y):
           path.append((cell.x, cell.y))
           cell = cell.parent
      
       path.append((end.x, end.y))
      
       #print(path)

       steps = 0
       for i in range(1, len(path)):
          
           next_x_coordinate = path[i][0]
           next_y_coordinate = path[i][1]
          
           if grid[next_y_coordinate][next_x_coordinate] == 0:
               cells[(next_x_coordinate, next_y_coordinate)].g_value = float('inf')
               cells[(next_x_coordinate, next_y_coordinate)].f_value = float('inf')
               break


           else:
               steps += 1
               current = cells[(next_x_coordinate, next_y_coordinate)]
               master_path.append((next_x_coordinate, next_y_coordinate))

               neighbors = [(current.x, current.y - 1), (current.x, current.y + 1), (current.x - 1, current.y), (current.x + 1, current.y)]


               for neighbor in neighbors:
                   if (neighbor[0] >= 0 and neighbor[0] < number_columns and neighbor[1] >= 0 and neighbor[1] < number_rows):
                       if grid[neighbor[1]][neighbor[0]] == 0:
                           if neighbor in cells:
                               cells[neighbor].g_value = float('inf')
                               cells[neighbor].f_value = float('inf')
                           else:
                               temp_cell = Cell(initial, current)
                               temp_cell.g_value = float('inf')
                               #temp_cell.h_value = manhattanDistance(temp_cell, start)
                               temp_cell.f_value = temp_cell.g_value
                               cells[neighbor] = temp_cell

   #print(master_path)
   return master_path

def manhattanDistance(current, end):
   return abs(end.x - current.x) + abs(end.y - current.y)

if __name__ == "__main__":
  
   gridObject = Grid()
   start = (0, 0)
   end = (100, 100)

   gridObject.create_new_maze()
   gridObject.display_maze()

#    path_to_color = repeated_forward_AStar(start, end, gridObject.grid)
#    gridObject.highlight_path(path_to_color)

#    path_to_color = repeated_backward_AStar(start, end, gridObject.grid)
#    gridObject.highlight_path(path_to_color)

   path_to_color = repeated_adaptive_AStar(start, end, gridObject.grid)
   gridObject.highlight_path(path_to_color)
  
   forwardCellsExpanded = []
   forwardTime = []
   backwardCellsExpanded = []
   backwardTime = []
   adaptiveCellsExpanded = []
   adaptiveTime = []
  
   for i in range(50):
       gridObject.create_new_maze()   

    #    # forward
    #    cells_expanded = 0
    #    startTime = time.time()
    #    repeated_forward_AStar(start, end, gridObject.grid)
    #    endTime = time.time()

    #    forwardCellsExpanded.append(cells_expanded)
    #    forwardTime.append(endTime - startTime)
          
       # backward
    #    cells_expanded = 0
    #    startTime = time.time()
    #    repeated_backward_AStar(start, end, gridObject.grid)
    #    endTime = time.time()


    #    backwardCellsExpanded.append(cells_expanded)
    #    backwardTime.append(endTime - startTime)

       
       # adaptive
       cells_expanded = 0
       startTime = time.time()
       repeated_adaptive_AStar(start, end, gridObject.grid)
       endTime = time.time()
      
       adaptiveCellsExpanded.append(cells_expanded)
       adaptiveTime.append(endTime - startTime)
        
  
  
   print("")
   print("ADAPTIVE A* STATISTICS:")
   print("Cells Expanded Mean: " + str(round(mean(adaptiveCellsExpanded), 4)))
   print("Cells Expanded Std Dev: " + str(round(stdev(adaptiveCellsExpanded), 4)))
   print("Runtime Mean: " + str(round(mean(adaptiveTime), 4)) + " s")
   print("Runtime Std Dev: " + str(round(stdev(adaptiveTime), 4)) + " s")

'''

   print("")
   print("FORWARD A* STATISTICS (Small G-Values):")
   print("Cells Expanded Mean: " + str(round(mean(forwardCellsExpanded), 4)))
   print("Cells Expanded Std Dev: " + str(round(stdev(forwardCellsExpanded), 4)))
   print("Runtime Mean: " + str(round(mean(forwardTime), 4)) + " s")
   print("Runtime Std Dev: " + str(round(stdev(forwardTime), 4)) + "s")

   print("")
   print("BACKWARD A* STATISTICS:")
   print("Cells Expanded Mean: " + str(round(mean(backwardCellsExpanded), 4)))
   print("Cells Expanded Std Dev: " + str(round(stdev(backwardCellsExpanded), 4)))
   print("Runtime Mean: " + str(round(mean(backwardTime), 4)) + " s")
   print("Runtime Std Dev: " + str(round(stdev(backwardTime), 4)) + " s")

'''
