import os
import copy
import queue
import time


def create_maze():
    maze = [["#", "#", "s", "#", "#"],
            [" ", " ", " ", "#", "#"],
            [" ", "#", " ", " ", "#"],
            [" ", "#", "#", " ", "#"],
            [" ", " ", " ", "f", "#"]]
    return maze


def maze_ended(maze, path):
    for x in range(len(maze[0])):
        if maze[0][x] == "s":
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

    return maze[current_y][current_x] == "f"


def valid(maze, path):
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

    for x in range(len(maze[0])):
        if maze[0][x] == "s":
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

    if not (-1 < current_x < len(maze[0]) and -1 < current_y < len(maze)):
        return False
    elif maze[current_y][current_x] == "#":
        return False
    else:
        return True


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_maze(maze, path):
    maze = copy.deepcopy(maze)

    for x in range(len(maze[0])):
        if maze[0][x] == "s":
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

        maze[current_y][current_x] = "+"

    clear_screen()
    print(*(' '.join(row) for row in maze), sep='\n')


def main():
    path = queue.Queue()
    path.put("")
    current_path = ""
    maze = create_maze()
    directions = ["R", "L", "U", "D"]

    while not maze_ended(maze, current_path):
        print_maze(maze, current_path)
        time.sleep(0.5)
        current_path = path.get()
        for direction in directions:
            new_path = current_path + direction
            if valid(maze, new_path):
                path.put(new_path)

    print_maze(maze, current_path)
    print(f"Shortest path: {current_path}")


if __name__ == '__main__':
    main()
