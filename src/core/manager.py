"""Менеджер лабиринтов и алгоритмов (заглушка)."""

# TODO: реализовать класс MazeManager для загрузки/генерации лабиринтов и запуска алгоритмов

import os
import sys
import time

import yaml

SRC_DIR = os.path.dirname(os.path.dirname(__file__))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from core.algorithms.astar import Astar, chebyshev
from core.maze import Maze
from utils.maze_generator import generate_maze, write_maze_to_config

maze = generate_maze(50, 20, (1,1), (40, 18))
write_maze_to_config("gen_maze", maze)

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



config_path = "config/config.yaml"
maze_key = "gen_maze"

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
