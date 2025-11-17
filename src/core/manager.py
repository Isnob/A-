import os
import sys
import time
import yaml

from src.core.algorithms.astar import Astar, chebyshev
from src.core.maze import Maze
from src.utils.maze_generator import generate_maze, write_maze_to_config



class Manager():

    def __init__(self):
        pass

    @staticmethod
    def _render_maze(maze, path, status):
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

    @staticmethod
    def generate_and_write_maze(name, config_path):
        maze = generate_maze(50, 20, (1,1), (40, 18))
        write_maze_to_config(name, maze, config_path)

    @staticmethod
    def delete_maze(name, config_path):
        with open(config_path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        if name in data:
            del data[name]
            with open(config_path, "w", encoding="utf-8") as fh:
                yaml.safe_dump(data, fh, allow_unicode=True, default_flow_style=False, sort_keys=False, indent=2,)


    def start_simulation(self, maze_name, config_path):

        with open(config_path, "r") as file:
            data = yaml.safe_load(file)

        maze = Maze(data, maze_name)
        astar = Astar(maze, chebyshev)

        while True:
            status, path = astar.step()
            self._render_maze(maze, path or [], status)
            if status != "IN PROCESS":
                break
            time.sleep(0.02)
