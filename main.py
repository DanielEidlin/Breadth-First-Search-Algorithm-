import os
import copy
import time
import queue
import datetime
from game2dboard import Board


class Algorithm(object):

    def __init__(self):
        self.path = queue.Queue()
        self.path.put("")
        self.current_path = ""
        self.maze = self.create_maze()
        self.directions = ["R", "L", "U", "D"]

    @staticmethod
    def create_maze():
        maze = [["#", "#", "s", "#", "#"],
                [" ", " ", " ", "#", "#"],
                [" ", "#", " ", " ", "#"],
                [" ", "#", "#", " ", "#"],
                [" ", " ", " ", "f", "#"]]
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

        for x in range(len(self.maze[0])):
            if self.maze[0][x] == "s":
                start_x = x
                break

        current_x = start_x
        current_y = 0

        for i, direction in enumerate(path):
            if direction == "R":
                current_x += 1
            elif direction == "L":
                current_x -= 1
            elif direction == "U":
                current_y -= 1
            elif direction == "D":
                current_y += 1
            else:
                raise ValueError(f"Direction: {direction} maze[{i}] is not a valid direction!")

        if not (-1 < current_x < len(self.maze[0]) and -1 < current_y < len(self.maze)):
            return False
        elif self.maze[current_y][current_x] == "#":
            return False
        else:
            return True

    def maze_ended(self):
        for x in range(len(self.maze[0])):
            if self.maze[0][x] == "s":
                start_x = x
                break

        current_x = start_x
        current_y = 0

        for i, direction in enumerate(self.current_path):
            if direction == "R":
                current_x += 1
            elif direction == "L":
                current_x -= 1
            elif direction == "U":
                current_y -= 1
            elif direction == "D":
                current_y += 1
            else:
                raise ValueError(f"Direction: {direction} maze[{i}] is not a valid direction!")

        return self.maze[current_y][current_x] == "f"

    def print_maze(self):
        maze_copy = copy.deepcopy(self.maze)

        for x in range(len(maze_copy[0])):
            if maze_copy[0][x] == "s":
                start_x = x
                break

        current_x = start_x
        current_y = 0

        for i, direction in enumerate(self.current_path):
            if direction == "R":
                current_x += 1
            elif direction == "L":
                current_x -= 1
            elif direction == "U":
                current_y -= 1
            elif direction == "D":
                current_y += 1
            else:
                raise ValueError(f"Direction: {direction} path[{i}] is not a valid direction!")

            maze_copy[current_y][current_x] = "+"

        self.clear_screen()
        print(*(' '.join(row) for row in maze_copy), sep='\n')
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
            self.show_maze(maze_to_show)
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


if __name__ == '__main__':
    algorithm = Algorithm()
    board = Board(len(algorithm.maze), len(algorithm.maze[0]))
    board.title = "Breadth First Search Algorithm Simulator"
    board.cell_size = 150
    board.on_timer = algorithm.main
    board.create_output(background_color="wheat4", color="white")
    board.start_timer(500)
    start_time = time.time()
    board.show()
