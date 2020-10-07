import os
import copy
import time
import queue
from tkinter import *
from typing import List
from PIL import Image, ImageTk
from random import randrange, shuffle


class MazeAlgorithm(object):

    def __init__(self, maze_width, maze_height):
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.path = queue.Queue()
        self.path.put("")
        self.current_path = ""
        self.maze = self.create_maze(self.maze_width, self.maze_height)
        self.directions = ["R", "L", "U", "D"]
        self.root = self.create_root()
        self.canvas = self.create_canvas()
        self.text = self.canvas.create_text((self.canvas.winfo_width() - 40) / 2, self.canvas.winfo_height() - 40,
                                            fill="white", text="")
        self.line_length = min((self.canvas.winfo_height() - 40) / (len(self.maze) / 2 - 1),
                               (self.canvas.winfo_width() - 40) / (len(self.maze[0]) - 1))
        self.total_time = 0
        self.graphics = []
        self.running = True
        self.start_image = self.generate_image("images/start.png")
        self.finish_image = self.generate_image('images/finish.png')
        self.right_image = self.generate_image('images/right.png')
        self.left_image = self.generate_image('images/left.png')
        self.up_image = self.generate_image('images/up.png')
        self.down_image = self.generate_image('images/down.png')

    def create_root(self) -> Tk:
        """
        Creates the root tkinter window.
        :return: Tk object.
        """
        root = Tk()
        root.title("Maze Generator and Solver Simulation")
        root.protocol("WM_DELETE_WINDOW", self.on_close)
        root.update()
        return root

    def create_canvas(self) -> Canvas:
        """
        Create tkinter canvas.
        :return:
        """
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        canvas = Canvas(self.root, bg="black", width=screen_width * 0.9, height=screen_height * 0.9)
        canvas.pack()
        self.root.update()
        return canvas

    def generate_image(self, path: str) -> ImageTk.PhotoImage:
        """
        Generate a tkinter image and resize it appropriately.
        :param path: The path to the image.
        :return: A tkinter image.
        """
        image = ImageTk.PhotoImage(Image.open(path).resize((int(self.line_length * 0.5), int(self.line_length * 0.5))))
        return image

    def on_close(self):
        """
        Destroys the window and end the mainloop.
        :return:
        """
        self.root.destroy()
        self.running = False

    @staticmethod
    def generate_maze(width: int, height: int) -> (List[List[str]], List[List[str]]):
        """
        Generates a random maze using the Randomized depth-first search algorithm.
        https://en.wikipedia.org/wiki/Maze_generation_algorithm
        :param width: Maze width.
        :param height: Maze height.
        :return: 2 separate 2d lists representing the horizontal and vertical parts of the maze's body.
        """
        visited = [[0] * width + [1] for _ in range(height)]
        visited.append([1] * (width + 1))
        horizontal = [['+---'] * width + ['+'] for _ in range(height + 1)]
        vertical = [['|   '] * width + ['|'] for _ in range(height)]
        vertical.append([])

        def traverse(x: int, y: int) -> NONE:
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
        return horizontal, vertical

    @staticmethod
    def create_maze(width: int, height: int) -> List[List[str]]:
        """
        Create a 2d list where each element represents a part of the maze.
        :param width: Maze width.
        :param height: Maze height.
        :return: A 2d list of strings.
        """
        horizontal, vertical = MazeAlgorithm.generate_maze(width, height)
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
    def clear_screen() -> NONE:
        """
        Clear the console screen.
        :return:
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def reverse_step(path: List[str]) -> bool:
        """
        Check that the path isn't taking a step back.
        :param path: The set of moves to follow e.g Right, Right, Down, Up...
        :return: A boolean representing whether or not a step back was taken.
        """
        # Check that we are not making a reverse step
        if len(path) > 1:
            if path[-1] == "R" and path[-2] == "L":
                return True
            elif path[-1] == "L" and path[-2] == "R":
                return True
            elif path[-1] == "U" and path[-2] == "D":
                return True
            elif path[-1] == "D" and path[-2] == "U":
                return True

        return False

    @staticmethod
    def walk_path(path: List[str]) -> (int, int):
        """
        Walk through the given path.
        :param path: The set of moves to follow e.g Right, Right, Down, Up...
        :return: x, y end coordinates.
        """
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
        return current_x, current_y

    def collided(self, path: List[str], x: int, y: int) -> bool:
        """
        Check that that current coordinates don't collide with a wall or exit the bounds.
        :param path: The set of moves to follow e.g Right, Right, Down, Up...
        :param x: x coordinate.
        :param y: y coordinate.
        :return: A boolean representing whether or not a collision occurred.
        """
        if not (-1 < x < len(self.maze[0]) - 1 and -1 < y < len(self.maze) - 1):
            return True
        elif path[-1] == "R" and self.maze[y][x][0] == "|":
            return True
        elif path[-1] == "L" and self.maze[y][x + 1][0] == "|":
            return True
        elif path[-1] == "U" and self.maze[y + 1][x][1] == "-":
            return True
        elif path[-1] == "D" and self.maze[y - 1][x][1] == "-":
            return True
        else:
            return False

    def valid(self, path: List[str]) -> bool:
        """
        Check if the current path is valid e.g if it's not going through a wall.
        :param path: The set of moves to follow e.g Right, Right, Down, Up...
        :return: A boolean representing the validity of the move.
        """
        x, y = MazeAlgorithm.walk_path(path)
        return not MazeAlgorithm.reverse_step(path) and not self.collided(path, x, y)

    def maze_ended(self) -> bool:
        """
        Check if the path has reached the end of the maze.
        :return: A boolean representing representing whether or not the end has been reached.
        """
        x, y = MazeAlgorithm.walk_path(self.current_path)
        return x == len(self.maze[0]) - 2 and y == len(self.maze) - 3

    @staticmethod
    def insert_arrow(x: int, y: int, maze: List[List[str]], direction: str) -> NONE:
        """
        Inserts ascii arrow indication depending on the direction.
        :param x: column index.
        :param y: row index.
        :param maze: A 2d list where each element represents a part of the maze.
        :param direction: The direction of the arrow.
        :return:
        """
        if direction == "R":
            cell_string_as_list = list(maze[y][x])
            cell_string_as_list[2] = '>'
            maze[y][x] = ''.join(cell_string_as_list)
        elif direction == "L":
            cell_string_as_list = list(maze[y][x])
            cell_string_as_list[2] = '<'
            maze[y][x] = ''.join(cell_string_as_list)
        elif direction == "U":
            cell_string_as_list = list(maze[y][x])
            cell_string_as_list[2] = '^'
            maze[y][x] = ''.join(cell_string_as_list)
        elif direction == "D":
            cell_string_as_list = list(maze[y][x])
            cell_string_as_list[2] = 'v'
            maze[y][x] = ''.join(cell_string_as_list)

    def print_maze(self) -> List[List[str]]:
        """
        Insert characters at appropriate locations of the maze and return the new maze.
        :return: A copy of the original maze but with mark characters.
        """
        maze_copy = copy.deepcopy(self.maze)

        for i, direction in enumerate(self.current_path):
            x, y = MazeAlgorithm.walk_path(self.current_path[:i + 1])
            arrow_direction = self.current_path[i + 1] if i < len(self.current_path) - 1 else direction
            self.insert_arrow(x, y, maze_copy, arrow_direction)

        maze_copy[-3][-2] = '  F '

        self.clear_screen()
        print(*(''.join(row) for row in maze_copy), sep='\n')
        return maze_copy

    def draw_maze(self, maze_to_draw: List[List[str]] = None) -> NONE:
        """
        Draws the maze.
        :param maze_to_draw: A specific maze to draw.
        :return:
        """
        x = 20
        y = 20
        maze = maze_to_draw if maze_to_draw else self.maze

        for i, row in enumerate(maze):
            for col in row:
                if col == '+---':
                    self.canvas.create_line(x, y, x + self.line_length, y, fill="white")
                elif col[0] == '|':
                    self.canvas.create_line(x, y, x, y - self.line_length, fill="white")

                x += self.line_length
                self.canvas.pack()
            self.root.update()

            x = 20
            if i % 2 == 0:
                y += self.line_length

    def draw_path(self, maze: List[List[str]]) -> NONE:
        """
        Draws the marks along the path to the screen.
        :param maze: A 2d list where each element represents a part of the maze.
        :return:
        """
        x = 20
        y = 20

        # clear ovals
        while self.graphics:
            component = self.graphics.pop()
            self.canvas.delete(component)

        for i, row in enumerate(maze):
            for col in row:
                if len(col) > 2 and col[2] == '>':
                    arrow = self.canvas.create_image(x + 0.5 * self.line_length, y - 0.5 * self.line_length,
                                                     image=self.right_image)
                    self.graphics.append(arrow)

                elif len(col) > 2 and col[2] == '<':
                    arrow = self.canvas.create_image(x + 0.5 * self.line_length, y - 0.5 * self.line_length,
                                                     image=self.left_image)
                    self.graphics.append(arrow)

                elif len(col) > 2 and col[2] == '^':
                    arrow = self.canvas.create_image(x + 0.5 * self.line_length, y - 0.5 * self.line_length,
                                                     image=self.up_image)
                    self.graphics.append(arrow)

                elif len(col) > 2 and col[2] == 'v':
                    arrow = self.canvas.create_image(x + 0.5 * self.line_length, y - 0.5 * self.line_length,
                                                     image=self.down_image)
                    self.graphics.append(arrow)

                elif len(col) > 2 and col[2] == 'S':
                    self.canvas.create_image(x + 0.5 * self.line_length, y - 0.5 * self.line_length,
                                             image=self.start_image)

                elif len(col) > 2 and col[2] == 'F':
                    self.canvas.create_image(x + 0.5 * self.line_length, y - 0.5 * self.line_length,
                                             image=self.finish_image)

                x += self.line_length

            x = 20
            if i % 2 == 0:
                y += self.line_length

        self.canvas.pack()
        self.root.update()

    def show_time(self, delta_time: float) -> NONE:
        """
        Update the text log about the current time took and path.
        :param delta_time: The time passed from previous iteration of the algorithm.
        :return:
        """
        self.total_time += delta_time
        self.canvas.itemconfigure(self.text, text=f"Time took: {self.total_time} secs\nPath: {self.current_path}")
        self.canvas.pack()
        self.root.update()

    def main(self) -> NONE:
        """
        The main function which solves the maze using the "breadth first search" algorithm.
        https://youtu.be/hettiSrJjM4
        Prints each attempt to the console and draws it on the screen.
        :return:
        """
        start_time = time.time()
        while not self.maze_ended():
            current_maze = self.print_maze()
            self.draw_path(maze=current_maze)
            gui_time = time.time()
            self.current_path = self.path.get()
            for direction in self.directions:
                new_path = self.current_path + direction
                if self.valid(new_path):
                    self.path.put(new_path)

            algorithm_time = time.time()
            self.show_time(algorithm_time - start_time - (algorithm_time - gui_time))
            start_time = time.time()

        current_maze = self.print_maze()
        self.draw_path(maze=current_maze)
        print(f"Shortest path: {self.current_path}")

        while self.running:
            self.root.update()


if __name__ == '__main__':
    algorithm = MazeAlgorithm(maze_width=20, maze_height=10)
    algorithm.draw_maze()
    algorithm.main()
