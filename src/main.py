import time

import yaml
from core.manager import 
from core.algorithms.astar import Astar, chebyshev
from core.maze import Maze


def render_maze(maze, path, status):
    path
    rows = []
    for y in range(maze.length):
        line = []
        for x in range(maze.width):
            node = maze.grid[y][x]
            pos = (x, y)
            if pos == maze.start:
                line.append('S')
            elif pos == maze.finish:
                line.append('F')
            elif node.type == "wall":
                line.append('\033[31mo\033[0m')
            elif pos in path:
                line.append('█')
            else:
                line.append(' ')
        rows.append(' '.join(line))
    print("\033[H\033[J", end="")
    print(f"Status: {status}")
    print('\n'.join(rows))


def main():


    config_path = "config/config.yaml"
    maze_key = "maze"

    with open(config_path, "r") as file:
        data = yaml.safe_load(file)

    maze = Maze(data, maze_key)
    astar = Astar(maze, chebyshev)

    while True:
        status, path = astar.step()
        render_maze(maze, path or [], status)
        if status != "IN PROCESS":
            break
        time.sleep(0.02)


if __name__ == "__main__":
    main()
