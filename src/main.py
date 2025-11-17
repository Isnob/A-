import argparse
import random
import time

import yaml

from core.algorithms.astar import Maze, Astar, chebyshev


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


def generate_noise_maze(width, height, wall_probability):
    grid = []
    start = (1, 1)
    finish = (width - 2, height - 2)

    for y in range(height):
        row = []
        for x in range(width):
            if x == 0 or y == 0 or x == width - 1 or y == height - 1:
                row.append(1)
            elif (x, y) == start:
                row.append('S')
            elif (x, y) == finish:
                row.append('F')
            else:
                row.append(1 if random.random() < wall_probability else 0)
        grid.append(row)

    return grid


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generate", action="store_true", help="generate noisy maze instead of using config")
    parser.add_argument("--width", type=int, default=100, help="width for generated maze")
    parser.add_argument("--height", type=int, default=100, help="height for generated maze")
    parser.add_argument("--wall-probability", type=float, default=0.45, help="wall density for generated maze")
    parser.add_argument("--seed", type=int, help="optional random seed for reproducible mazes")
    parser.add_argument("--config", default="config/config.yaml", help="path to config file with maze data")
    parser.add_argument("--maze-key", default="maze", help="key of maze data inside config file")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.seed is not None:
        random.seed(args.seed)

    if args.generate:
        data = {args.maze_key: generate_noise_maze(args.width, args.height, args.wall_probability)}
    else:
        data = yaml.safe_load(open(args.config))

    name_maze = args.maze_key
    maze = Maze(data, name_maze)
    astar = Astar(maze, chebyshev)

    while True:
        status, path = astar.step()
        render_maze(maze, path or [], status)
        if status != "IN PROCESS":
            break
        time.sleep(0.02)


if __name__ == "__main__":
    main()
