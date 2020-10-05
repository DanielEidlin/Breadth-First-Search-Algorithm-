import os
import copy
import sys
import time
import queue
import pygame
import datetime
from pygame.locals import *
from random import randrange, shuffle

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Algorithm(object):

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.path = queue.Queue()
        self.path.put("")
        self.current_path = ""
        self.maze = self.create_maze(self.width, self.height)
        self.directions = ["R", "L", "U", "D"]

    @staticmethod
    def create_maze(width, height):
        visited = [[0] * width + [1] for _ in range(height)]
        visited.append([1] * (width + 1))
        horizontal = [['+---'] * width + ['+'] for _ in range(height + 1)]
        vertical = [['|   '] * width + ['|'] for _ in range(height)]
        vertical.append([])

        def traverse(x, y):
            visited[y][x] = 1
            neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            shuffle(neighbours)
            for neighbour in neighbours:
                if visited[neighbour[1]][neighbour[0]]:
                    continue
                elif neighbour[0] == x:
                    horizontal[max(neighbour[1], y)][x] = '+   '
                elif neighbour[1] == y:
                    vertical[y][max(neighbour[0], x)] = '    '

                traverse(neighbour[0], neighbour[1])

        traverse(randrange(width), randrange(height))

        maze = []
        for i in range(len(horizontal)):
            maze.append(horizontal[i])
            maze.append(vertical[i])

        # Mark start and finish point
        maze[1][0] = '| S '
        maze[-3][-2] = '  F '
        cell_string_as_list = list(maze[-3][-2])
        cell_string_as_list[2] = 'F'
        maze[-3][-2] = ''.join(cell_string_as_list)

        return maze

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def valid(self, path):
        # Check that we are not making a reverse step
        if len(path) > 1:
            if path[-1] == "R" and path[-2] == "L":
                return False
            elif path[-1] == "L" and path[-2] == "R":
                return False
            elif path[-1] == "U" and path[-2] == "D":
                return False
            elif path[-1] == "D" and path[-2] == "U":
                return False

        current_x = 0
        current_y = 1
        for i, direction in enumerate(path):
            if direction == "R":
                current_x += 1
            elif direction == "L":
                current_x -= 1
            elif direction == "U":
                current_y -= 2
            elif direction == "D":
                current_y += 2
            else:
                raise ValueError(f"Direction: {direction} maze[{i}] is not a valid direction!")

        if not (-1 < current_x < len(self.maze[0]) - 1 and -1 < current_y < len(self.maze) - 1):
            return False
        elif path[-1] == "R" and self.maze[current_y][current_x][0] == "|":
            return False
        elif path[-1] == "L" and self.maze[current_y][current_x + 1][0] == "|":
            return False
        elif path[-1] == "U" and self.maze[current_y + 1][current_x][1] == "-":
            return False
        elif path[-1] == "D" and self.maze[current_y - 1][current_x][1] == "-":
            return False
        else:
            return True

    def maze_ended(self):
        current_x = 0
        current_y = 1

        for i, direction in enumerate(self.current_path):
            if direction == "R":
                current_x += 1
            elif direction == "L":
                current_x -= 1
            elif direction == "U":
                current_y -= 2
            elif direction == "D":
                current_y += 2
            else:
                raise ValueError(f"Direction: {direction} maze[{i}] is not a valid direction!")

        return current_x == len(self.maze[0]) - 2 and current_y == len(self.maze) - 3

    def print_maze(self):
        maze_copy = copy.deepcopy(self.maze)
        current_x = 0
        current_y = 1

        for i, direction in enumerate(self.current_path):
            if direction == "R":
                current_x += 1
            elif direction == "L":
                current_x -= 1
            elif direction == "U":
                current_y -= 2
            elif direction == "D":
                current_y += 2
            else:
                raise ValueError(f"Direction: {direction} path[{i}] is not a valid direction!")

            cell_string_as_list = list(maze_copy[current_y][current_x])
            cell_string_as_list[2] = '*'
            maze_copy[current_y][current_x] = ''.join(cell_string_as_list)

        self.clear_screen()
        print(*(''.join(row) for row in maze_copy), sep='\n')
        return maze_copy

    def main2(self):
        while not self.maze_ended():
            self.print_maze()
            time.sleep(0.2)
            self.current_path = self.path.get()
            for direction in self.directions:
                new_path = self.current_path + direction
                if self.valid(new_path):
                    self.path.put(new_path)

        self.print_maze()
        print(f"Shortest path: {self.current_path}")

    def draw_maze(self, width, height):
        """
        Draws the maze.
        :param width: window width.
        :param height: window height.
        :return:
        """
        x = 20
        y = 20
        line_width = min((height-40) / (len(self.maze)/2 - 1), (width-40) / (len(self.maze[0])-1))
        for i, row in enumerate(self.maze):
            for col in row:
                if col == '+---':
                    pygame.draw.line(board, WHITE, (x, y), (x + line_width, y))
                elif col[0] == '|':
                    pygame.draw.line(board, WHITE, (x, y), (x, y - line_width))
                else:
                    pass
                x += line_width
            x = 20
            if i % 2 == 0:
                y += line_width


if __name__ == '__main__':
    algorithm = Algorithm(width=40, height=20)
    # algorithm.main2()
    pygame.init()
    info_object = pygame.display.Info()
    board = pygame.display.set_mode((info_object.current_w - 100, info_object.current_h - 100))
    board.fill(BLACK)
    pygame.display.set_caption("Maze Generator and Solver Simulation")
    clock = pygame.time.Clock()
    algorithm.draw_maze(board.get_width(), board.get_height())
    # pygame main loop
    while True:
        # code...
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(30)
