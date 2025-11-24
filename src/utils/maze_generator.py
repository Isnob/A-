import random
import yaml

def generate_maze(width, height, start, finish, density=0.5):
    maze = []
    for y in range(height):
        row = []
        for x in range(width):
            if y in (0, height - 1) or x in (0, width - 1):
                row.append(1)
            else:
                row.append(1 if random.random() < density else 0)
        maze.append(row)

    sx, sy = start
    fx, fy = finish
    maze[sy][sx] = "S"
    maze[fy][fx] = "F"
    return ["".join(str(cell) for cell in row) for row in maze]


def write_maze_to_config(name, maze, config_path):
    with open(config_path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    data[name] = maze
    with open(config_path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(
            data,
            fh,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
        )
