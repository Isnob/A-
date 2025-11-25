import time
import yaml

from src.core.algorithms.astar import Astar, chebyshev
from src.core.algorithms.bfs import BFS
from src.core.algorithms.dijkstra import Dijkstra
from src.core.maze import Maze
from src.utils.maze_generator import generate_maze, write_maze_to_config


class Manager:

    def __init__(self):
        pass

    @staticmethod
    def _render_maze(maze, path, status, visited=None, frontier=None, current=None):
        visited = visited or set()
        frontier = frontier or set()
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
                elif pos == current:
                    line.append('\033[93mX\033[0m') 
                elif pos in path:
                    line.append('█')
                elif pos in frontier:
                    line.append('\033[36m*\033[0m')   # граница
                elif pos in visited:
                    line.append('\033[90m.\033[0m')
                else:
                    line.append(' ')
            rows.append(' '.join(line))

        print("\033[H\033[J", end="")
        print(f"Status: {status}")
        print('\n'.join(rows))

    @staticmethod
    def generate_and_write_maze(
        name,
        config_path,
        width=50,
        height=20,
        start=(1, 1),
        finish=(40, 18),
        density=0.5,
    ):
        maze = generate_maze(width, height, start, finish, density=density)
        write_maze_to_config(name, maze, config_path)

    @staticmethod
    def delete_maze(name, config_path):
        with open(config_path, "r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        if name in data:
            del data[name]
            with open(config_path, "w", encoding="utf-8") as fh:
                yaml.safe_dump(
                    data,
                    fh,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False,
                    indent=2,
                )

    @staticmethod
    def _create_solver(algorithm: str, maze: Maze):
        algorithm = algorithm.lower()
        if algorithm == "astar":
            return Astar(maze, chebyshev)
        if algorithm == "bfs":
            return BFS(maze)
        if algorithm == "dijkstra":
            return Dijkstra(maze)
        raise ValueError(f"Unknown algorithm: {algorithm}")

    def start_simulation(self, maze_name, config_path, algorithm="astar"):
        """
        ГЛАВНЫЙ МЕТОД ДЛЯ GUI.

        - загружает Maze
        - создаёт solver
        - ничего не рисует
        - ничего не крутит
        - возвращает (maze, solver)
        """
        with open(config_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)

        maze = Maze(data, maze_name)
        solver = self._create_solver(algorithm, maze)
        return maze, solver

    def run_cli_simulation(self, maze_name, config_path, algorithm="astar", delay=0.5):
        maze, solver = self.start_simulation(
            maze_name=maze_name,
            config_path=config_path,
            algorithm=algorithm,
        )

        sleep_time = delay

        while True:
            status, path = solver.step()
            state = solver.get_state()

            self._render_maze(
                maze,
                path or set(),
                status,
                visited=state["visited"],
                frontier=state["frontier"],
                current=state["current"],
            )

            if status != "IN PROCESS":
                break
            time.sleep(sleep_time)
