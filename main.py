import os
import copy
import time
import queue
import datetime
from random import randrange, shuffle

from game2dboard import Board


class Algorithm(object):

    def __init__(self):
        self.path = queue.Queue()
        self.path.put("")
        self.current_path = ""
        self.maze = self.create_maze(width=16, height=9)
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
            neighbours = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
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

    def show_maze(self, maze):
        delta = datetime.timedelta(seconds=int(time.time() - start_time - 0.5))
        board.clear()
        board.print(f"Time took: {str(delta)}:{delta.microseconds}\tPath: {self.current_path}")
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                if maze[row][col] == "#":
                    board[row][col] = "wall"
                elif maze[row][col] == "+":
                    board[row][col] = "dot"
                elif maze[row][col] == "s":
                    board[row][col] = "start"
                elif maze[row][col] == "f":
                    board[row][col] = "finish"
                else:
                    pass

    def main(self):
        if not self.maze_ended():
            maze_to_show = self.print_maze()
            self.show_maze(maze_to_show)    # TODO: Update this!
            self.current_path = self.path.get()
            for direction in self.directions:
                new_path = self.current_path + direction
                if self.valid(new_path):
                    self.path.put(new_path)
        else:
            board.stop_timer()
            maze_to_show = self.print_maze()
            self.show_maze(maze_to_show)
            print(f"Shortest path: {self.current_path}")

    def main2(self):
        while not self.maze_ended():
            maze_to_show = self.print_maze()
            time.sleep(0.2)
            self.current_path = self.path.get()
            for direction in self.directions:
                new_path = self.current_path + direction
                if self.valid(new_path):
                    self.path.put(new_path)

        maze_to_show = self.print_maze()
        print(f"Shortest path: {self.current_path}")


if __name__ == '__main__':
    algorithm = Algorithm()
    algorithm.main2()
    # board = Board(len(algorithm.maze), len(algorithm.maze[0]))
    # board.title = "Breadth First Search Algorithm Simulator"
    # board.cell_size = 150
    # board.on_timer = algorithm.main
    # board.create_output(background_color="wheat4", color="white")
    # board.start_timer(500)
    # start_time = time.time()
    # board.show()
