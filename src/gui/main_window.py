from __future__ import annotations

import traceback

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QStatusBar,
    QMessageBox,
)

import yaml

from src.core.manager import Manager
from src.gui.controls_panel import ControlsPanel
from src.gui.maze_view import MazeView


class MainWindow(QMainWindow):
    """
    Главное окно:
    - слева панель управления (ControlsPanel)
    - справа визуализация лабиринта (MazeView)
    - снизу статус-бар
    """

    def __init__(self, config_path: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Pathfinding Visualizer")

        self.config_path = config_path
        self.manager = Manager()
        self.maze = None
        self.solver = None
        self.state = None
        self.iteration = 0


        self.current_maze_name: str | None = None
        self.current_algorithm_name: str = "astar"
        self.current_delay: float = 0.2  # секунды

        self._init_ui()
        self._init_timer()
        self._connect_signals()
        self._refresh_maze_list()

    # --- Инициализация UI ---

    def _init_ui(self) -> None:
        central = QWidget(self)
        layout = QHBoxLayout(central)

        self.controls = ControlsPanel(self)
        self.maze_view = MazeView(self)

        layout.addWidget(self.controls)
        layout.addWidget(self.maze_view, stretch=1)

        self.setCentralWidget(central)

        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        self.statusBar().showMessage("Готово")

    def _init_timer(self) -> None:
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_timer_tick)
        # интервал подстроится в on_speed_changed
        self.on_speed_changed(self.current_delay)

    def _connect_signals(self) -> None:
        c = self.controls

        c.generate_requested.connect(self.on_generate_requested)
        c.delete_requested.connect(self.on_delete_requested)
        c.refresh_requested.connect(self._refresh_maze_list)

        c.maze_selected.connect(self.on_maze_selected)
        c.algorithm_selected.connect(self.on_algorithm_selected)

        c.start_requested.connect(self.on_start_requested)
        c.pause_requested.connect(self.on_pause_requested)
        c.step_requested.connect(self.on_step_requested)
        c.reset_requested.connect(self.on_reset_requested)

        c.speed_changed.connect(self.on_speed_changed)

        c.import_requested.connect(self.on_import_requested)

    # --- Работа с менеджером / YAML ---

    def _load_maze_names(self) -> list[str]:
        try:
            with open(self.config_path, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            if isinstance(data, dict):
                return list(data.keys())
            return []
        except FileNotFoundError:
            return []
        except Exception as exc:
            print("Ошибка при чтении mazes yaml:", exc)
            traceback.print_exc()
            return []

    def _refresh_maze_list(self) -> None:
        names = self._load_maze_names()
        self.controls.set_maze_names(names)
        if names and self.current_maze_name not in names:
            self.current_maze_name = names[0]
        self.statusBar().showMessage("Список лабиринтов обновлён")

    def _create_solver(self) -> None:
        """
        Создаёт maze и solver через Manager.start_simulation.
        Никаких циклов, только инициализация.
        """
        if not self.current_maze_name:
            QMessageBox.warning(self, "Нет лабиринта", "Сначала выбери лабиринт.")
            return
        
        self.iteration = 0

        try:
            maze, solver = self.manager.start_simulation(
                maze_name=self.current_maze_name,
                config_path=self.config_path,
                algorithm=self.current_algorithm_name,
                delay=self.current_delay,
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось создать алгоритм:\n{exc}",
            )
            traceback.print_exc()
            return

        self.maze = maze
        self.solver = solver
        self.state = None

        self.maze_view.set_maze(maze)
        self.statusBar().showMessage(
            f"Алгоритм: {self.current_algorithm_name}, лабиринт: {self.current_maze_name}"
        )

    # --- Слоты от панели управления ---

    def on_generate_requested(self, name, width, height, density, start, finish):
        try:
            # старт и финиш пока заглушка — ты потом поправишь
            self.manager.generate_and_write_maze(
                name=name,
                config_path=self.config_path,
                width=width,
                height=height,
                start=start,
                finish=finish,
                density=density,
            )
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Ошибка генерации",
                f"Не удалось сгенерировать лабиринт:\n{exc}",
            )
            traceback.print_exc()
            return

        self._refresh_maze_list()
        self.statusBar().showMessage(f"Лабиринт '{name}' сгенерирован")

    def on_delete_requested(self, name: str) -> None:
        try:
            self.manager.delete_maze(name, self.config_path)
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Ошибка удаления",
                f"Не удалось удалить лабиринт:\n{exc}",
            )
            traceback.print_exc()
            return

        if self.current_maze_name == name:
            self.current_maze_name = None
            self.maze = None
            self.solver = None
            self.state = None
            self.maze_view.clear()

        self._refresh_maze_list()
        self.statusBar().showMessage(f"Лабиринт '{name}' удалён")

    def on_maze_selected(self, name: str) -> None:
        self.current_maze_name = name
        self.statusBar().showMessage(f"Выбран лабиринт: {name}")

    def on_algorithm_selected(self, algorithm_code: str) -> None:
        self.current_algorithm_name = algorithm_code
        self.statusBar().showMessage(f"Выбран алгоритм: {algorithm_code}")

    def on_start_requested(self) -> None:
        if self.solver is None or self.maze is None:
            self._create_solver()
            if self.solver is None:
                return

        if not self.timer.isActive():
            self.timer.start()
            self.statusBar().showMessage("Симуляция запущена")

    def on_pause_requested(self) -> None:
        if self.timer.isActive():
            self.timer.stop()
            self.statusBar().showMessage("Симуляция на паузе")

    def on_step_requested(self) -> None:
        if self.solver is None or self.maze is None:
            self._create_solver()
            if self.solver is None:
                return
        # один шаг без запуска таймера
        self._on_timer_tick()

    def on_reset_requested(self) -> None:
        self.timer.stop()
        self._create_solver()
        self.statusBar().showMessage("Симуляция сброшена")

    def on_speed_changed(self, delay_seconds: float) -> None:
        """
        delay_seconds — задержка между шагами в секундах.
        """
        self.current_delay = max(0.0, float(delay_seconds))
        self.timer.setInterval(int(self.current_delay * 1000))

        # если захочешь, можно ещё передавать delay в solver
        if self.solver is not None and hasattr(self.solver, "set_delay"):
            try:
                self.solver.set_delay(self.current_delay)
            except Exception:
                # не критично
                pass

    def on_import_requested(self) -> None:
        # Заглушка под будущее.
        # Здесь потом сделаешь диалог выбора файла и запись лабиринта в YAML.
        QMessageBox.information(
            self,
            "Импорт",
            "Импорт лабиринта ещё не реализован.",
        )

    # --- Таймер / шаги алгоритма ---

    def _on_timer_tick(self) -> None:

        self.iteration += 1

        if self.solver is None or self.maze is None:
            self.timer.stop()
            return

        try:
            result = self.solver.step()
        except Exception as exc:
            self.timer.stop()
            QMessageBox.critical(
                self,
                "Ошибка алгоритма",
                f"Исключение в step():\n{exc}",
            )
            traceback.print_exc()
            return

        # поддержка двух вариантов: (status, path) и только status
        if isinstance(result, tuple) and len(result) == 2:
            status, path = result
        else:
            status = result
            path = set()

        # если алгоритм уже реализует get_state() — используем его
        state = {
            "path": path or set(),
            "visited": set(),
            "frontier": set(),
            "current": None,
        }
        if hasattr(self.solver, "get_state"):
            try:
                solver_state = self.solver.get_state() or {}
                # подстрахуемся, если там нет path
                if "path" not in solver_state:
                    solver_state["path"] = state["path"]
                state.update(solver_state)
            except Exception:
                # если get_state сломан — работаем с дефолтным state
                traceback.print_exc()

        state["status"] = status
        self.state = state

        self.maze_view.update_state(self.maze, state)
        self.statusBar().showMessage(
            f"Status: {status} | Path len: {len(state["path"])} | Iter: {self.iteration} | Path len: {len(state['path'])}"
            )


        if status != "IN PROCESS":
            self.timer.stop()
