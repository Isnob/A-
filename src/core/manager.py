import os
import sys
import time
import yaml

from src.core.algorithms.astar import Astar, chebyshev
from src.core.algorithms.bfs import BFS
from src.core.algorithms.dijkstra import Dijkstra
from src.core.maze import Maze
from src.utils.maze_generator import generate_maze, write_maze_to_config



class Manager():

    def __init__(self, delay=0.02):
        self.delay = delay

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


    def start_simulation(self, maze_name, config_path, algorithm="astar", delay=None):

        with open(config_path, "r") as file:
            data = yaml.safe_load(file)

        if delay is not None:
            self.delay = max(0.0, float(delay))
        sleep_time = self.delay
        algorithm = algorithm.lower()
        iters = 0

        match algorithm:

            case "astar":
                maze = Maze(data, maze_name)
                solver = Astar(maze, chebyshev)
            case "bfs":
                maze = Maze(data, maze_name)
                solver = BFS(maze)
            case "dijkstra":
                maze = Maze(data, maze_name)
                solver = Dijkstra(maze)
            case _:
                raise ValueError(f"Unknown algorithm: {algorithm}")

        while True:
            iters += 1
            status, path = solver.step()
            self._render_maze(maze, path or [], status)
            if status != "IN PROCESS":
                break
            time.sleep(sleep_time)
