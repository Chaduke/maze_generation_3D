# maze.py
# Referenced from - https://inventwithpython.com/recursion/chapter11.html
# adapted for LibSGD by Chaduke
# https://chaduke.github.io/support-me
# 20240918

import random
from libsgd import sgd
from math import sin,cos

class Maze:
    def __init__(self,_width,_height,_seed):
        self.WIDTH = _width  # Width of the maze (must be odd).
        self.HEIGHT = _height  # Height of the maze (must be odd).
        assert self.WIDTH % 2 == 1 and self.WIDTH >= 3
        assert self.HEIGHT % 2 == 1 and self.HEIGHT >= 3
        self.SEED = _seed
        random.seed(self.SEED)
        # Use these characters for displaying the maze:
        self.EMPTY = ' '
        self.MARK = '@'
        self.WALL = chr(9608)  # Character 9608 is '█'
        self.NORTH, self.SOUTH, self.EAST, self.WEST = 'n', 's', 'e', 'w'

        # Create the filled-in maze data structure to start:
        self.maze = {}
        # Carve out the paths in the maze data structure:
        self.hasVisited = [(1, 1)]  # Start by visiting the top-left corner.

        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                self.maze[(x, y)] = self.WALL  # Every space is a wall at first.
                
        self.unvisitedNeighbors = []
        self.grid_size = 6

    def print_maze(self,mark_x=None, mark_y=None):
        """Displays the maze data structure in the maze argument. The
        mark_x and mark_y arguments are coordinates of the current
        '@' location of the algorithm as it generates the maze."""
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if mark_x == x and mark_y == y:
                    # Display the '@' mark here:
                    print(self.MARK, end='')
                else:
                    # Display the wall or empty space:
                    print(self.maze[(x, y)], end='')
            print()  # Print a newline after printing the row.
    def draw2d(self,offset_x,offset_y,_player):
        yw = self.WIDTH * self.grid_size
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                # Display the wall

                if self.maze[(x, y)] != ' ':
                    sgd.set2DFillColor(0, 0, 1, 1)
                    sgd.draw2DRect(x * self.grid_size - self.grid_size / 2 + offset_x,
                                   yw - (y * self.grid_size - self.grid_size / 2 + offset_y),
                                   x * self.grid_size + self.grid_size / 2 + offset_x,
                                   yw - (y * self.grid_size + self.grid_size / 2 + offset_y))
        px = sgd.getEntityX(_player.pivot) * self.grid_size + offset_x
        # reverse the direction when converting Z-axis in 3D to Y-axis in 2D
        py = yw - sgd.getEntityZ(_player.pivot) * self.grid_size + offset_y
        sgd.set2DFillColor(1, 0, 0, 1)
        sgd.draw2DLine(px, py, px + sin((sgd.getEntityRY(_player.pivot) - 180) * 0.0174533) * 8,
                       py + cos((sgd.getEntityRY(_player.pivot) - 180) * 0.0174533) * 8)
        sgd.set2DFillColor(1, 1, 0, 1)
        sgd.draw2DOval(px - 3, py - 3, px + 3, py + 3)

    def create_blocks(self):
        box_material = sgd.loadPBRMaterial("sgd://materials/Bricks076C_1K-JPG")
        mesh = sgd.createBoxMesh(-0.5,-0.5,-0.5,0.5,0.5,0.5,box_material)
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.maze[(x, y)] != ' ':
                    cube = sgd.createModel(mesh)
                    sgd.setEntityPosition(cube,x,0.5,y)
                    sgd.createMeshCollider(cube,0,mesh)

    def visit(self,x, y):
        """"Carve out" empty spaces in the maze at x, y and then
        recursively move to neighboring unvisited spaces. This
        function backtracks when the mark has reached a dead end."""
        self.maze[(x, y)] = self.EMPTY  # "Carve out" the space at x, y.
        #self.print_maze(x, y)  # Display the maze as we generate it.
        #print('\n\n')

        while True:
            # Check which neighboring spaces adjacent to
            # the mark have not been visited already:
            self.unvisitedNeighbors.clear()
            if y > 1 and (x, y - 2) not in self.hasVisited:
                self.unvisitedNeighbors.append(self.NORTH)

            if y < self.HEIGHT - 2 and (x, y + 2) not in self.hasVisited:
                self.unvisitedNeighbors.append(self.SOUTH)

            if x > 1 and (x - 2, y) not in self.hasVisited:
                self.unvisitedNeighbors.append(self.WEST)

            if x < self.WIDTH - 2 and (x + 2, y) not in self.hasVisited:
                self.unvisitedNeighbors.append(self.EAST)

            if len(self.unvisitedNeighbors) == 0:
                # BASE CASE
                # All neighboring spaces have been visited, so this is a
                # dead end. Backtrack to an earlier space:
                return
            else:
                # RECURSIVE CASE
                # Randomly pick an unvisited neighbor to visit:
                next_intersection = random.choice(self.unvisitedNeighbors)

                # Move the mark to an unvisited neighboring space:
                next_x = 0
                next_y = 0
                if next_intersection == self.NORTH:
                    next_x = x
                    next_y = y - 2
                    self.maze[(x, y - 1)] = self.EMPTY  # Connecting hallway.
                elif next_intersection == self.SOUTH:
                    next_x = x
                    next_y = y + 2
                    self.maze[(x, y + 1)] = self.EMPTY  # Connecting hallway.
                elif next_intersection == self.WEST:
                    next_x = x - 2
                    next_y = y
                    self.maze[(x - 1, y)] = self.EMPTY  # Connecting hallway.
                elif next_intersection == self.EAST:
                    next_x = x + 2
                    next_y = y
                    self.maze[(x + 1, y)] = self.EMPTY  # Connecting hallway.

                self.hasVisited.append((next_x, next_y))  # Mark as visited.
                self.visit(next_x, next_y)  # Recursively visit this space.
