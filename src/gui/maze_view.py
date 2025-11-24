from __future__ import annotations

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from PyQt6.QtWidgets import QWidget


class MazeView(QWidget):
    """
    Виджет для отрисовки лабиринта и состояния алгоритма.
    Ожидает:
    - Maze с полями width, length, grid, start, finish
    - state: dict с ключами path, visited, frontier, current
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.maze = None
        self.path = set()
        self.visited = set()
        self.frontier = set()
        self.current = None

        self.color_background = QColor(30, 30, 30)
        self.color_wall = QColor(40, 40, 40)
        self.color_empty = QColor(220, 220, 220)
        self.color_start = QColor(0, 200, 0)
        self.color_finish = QColor(200, 0, 0)
        self.color_visited = QColor(150, 150, 255)
        self.color_frontier = QColor(255, 200, 0)
        self.color_path = QColor(0, 255, 100)
        self.color_current = QColor(255, 80, 80)

    def set_maze(self, maze) -> None:
        self.maze = maze
        self.path = set()
        self.visited = set()
        self.frontier = set()
        self.current = None
        self.update()

    def update_state(self, maze, state: dict) -> None:
        self.maze = maze
        self.path = set(state.get("path") or [])
        self.visited = set(state.get("visited") or [])
        self.frontier = set(state.get("frontier") or [])
        self.current = state.get("current")
        self.update()

    def clear(self) -> None:
        self.maze = None
        self.path.clear()
        self.visited.clear()
        self.frontier.clear()
        self.current = None
        self.update()

    def minimumSizeHint(self) -> QSize:
        return QSize(400, 300)

    def sizeHint(self) -> QSize:
        return QSize(600, 400)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        # фон
        painter.fillRect(self.rect(), self.color_background)

        if self.maze is None:
            return

        rows = getattr(self.maze, "length", 0)
        cols = getattr(self.maze, "width", 0)
        if rows <= 0 or cols <= 0:
            return

        cell_w = self.width() / cols
        cell_h = self.height() / rows
        cell_size = min(cell_w, cell_h)

        offset_x = (self.width() - cols * cell_size) / 2.0
        offset_y = (self.height() - rows * cell_size) / 2.0

        painter.setPen(QPen(Qt.GlobalColor.black))

        start_pos = getattr(self.maze, "start", None)
        finish_pos = getattr(self.maze, "finish", None)

        for y in range(rows):
            for x in range(cols):
                pos = (x, y)
                node = self.maze.grid[y][x]

                # базовый цвет
                if pos == start_pos:
                    color = self.color_start
                elif pos == finish_pos:
                    color = self.color_finish
                elif node.type == "wall":
                    color = self.color_wall
                else:
                    color = self.color_empty

                # состояние алгоритма — поверх
                if pos in self.visited and pos not in (start_pos, finish_pos):
                    color = self.color_visited

                if pos in self.frontier and pos not in (start_pos, finish_pos):
                    color = self.color_frontier

                if pos in self.path and pos not in (start_pos, finish_pos):
                    color = self.color_path

                if self.current is not None and pos == tuple(self.current):
                    color = self.color_current

                px = offset_x + x * cell_size
                py = offset_y + y * cell_size

                painter.setBrush(QBrush(color))
                painter.drawRect(int(px), int(py), int(cell_size), int(cell_size))
