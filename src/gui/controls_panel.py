from __future__ import annotations

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QComboBox,
    QSlider,
    QGroupBox,
)


class ControlsPanel(QWidget):
    """
    Панель управления:
    - выбор лабиринта
    - генерация / удаление
    - выбор алгоритма
    - управление симуляцией
    - слайдер скорости
    """

    generate_requested = pyqtSignal(str, int, int, float, tuple, tuple)
    delete_requested = pyqtSignal(str)
    refresh_requested = pyqtSignal()

    maze_selected = pyqtSignal(str)
    algorithm_selected = pyqtSignal(str)

    start_requested = pyqtSignal()
    pause_requested = pyqtSignal()
    step_requested = pyqtSignal()
    reset_requested = pyqtSignal()

    speed_changed = pyqtSignal(float)  # секунды

    import_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        # --- выбор лабиринта ---
        maze_group = QGroupBox("Лабиринты", self)
        maze_layout = QVBoxLayout(maze_group)

        self.combo_mazes = QComboBox(maze_group)
        self.btn_refresh = QPushButton("Обновить список", maze_group)
        self.btn_delete = QPushButton("Удалить выбранный", maze_group)
        self.btn_import = QPushButton("Импорт из файла...", maze_group)

        maze_layout.addWidget(QLabel("Выбрать лабиринт:", maze_group))
        maze_layout.addWidget(self.combo_mazes)
        maze_layout.addWidget(self.btn_refresh)
        maze_layout.addWidget(self.btn_delete)
        maze_layout.addWidget(self.btn_import)

        # --- генерация ---
        gen_group = QGroupBox("Генерация лабиринта", self)
        gen_layout = QVBoxLayout(gen_group)

        self.edit_name = QLineEdit(gen_group)
        self.edit_name.setPlaceholderText("Имя лабиринта")

        self.spin_width = QSpinBox(gen_group)
        self.spin_width.setRange(5, 200)
        self.spin_width.setValue(50)

        self.spin_height = QSpinBox(gen_group)
        self.spin_height.setRange(5, 200)
        self.spin_height.setValue(20)

        self.spin_start_x = QSpinBox();  self.spin_start_x.setRange(0, 999)
        self.spin_start_y = QSpinBox();  self.spin_start_y.setRange(0, 999)

        self.spin_finish_x = QSpinBox(); self.spin_finish_x.setRange(0, 999)
        self.spin_finish_y = QSpinBox(); self.spin_finish_y.setRange(0, 999)


        self.spin_density = QDoubleSpinBox(gen_group)
        self.spin_density.setRange(0.0, 1.0)
        self.spin_density.setSingleStep(0.05)
        self.spin_density.setValue(0.5)

        lbl_size = QLabel("Размер (ширина x высота):", gen_group)
        size_layout = QHBoxLayout()
        size_layout.addWidget(self.spin_width)
        size_layout.addWidget(self.spin_height)

        lbl_density = QLabel("Плотность стен (0..1):", gen_group)

        # ---- START / FINISH ----
        coords_group = QGroupBox("Старт / Финиш", self)
        coords_layout = QVBoxLayout(coords_group)

        # START
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Start X:", self))
        start_layout.addWidget(self.spin_start_x)
        start_layout.addWidget(QLabel("Y:", self))
        start_layout.addWidget(self.spin_start_y)

        # FINISH
        finish_layout = QHBoxLayout()
        finish_layout.addWidget(QLabel("Finish X:", self))
        finish_layout.addWidget(self.spin_finish_x)
        finish_layout.addWidget(QLabel("Y:", self))
        finish_layout.addWidget(self.spin_finish_y)

        coords_layout.addLayout(start_layout)
        coords_layout.addLayout(finish_layout)

        self.btn_generate = QPushButton("Сгенерировать", gen_group)

        gen_layout.addWidget(QLabel("Имя:", gen_group))
        gen_layout.addWidget(self.edit_name)
        gen_layout.addWidget(lbl_size)
        gen_layout.addLayout(size_layout)
        gen_layout.addWidget(lbl_density)
        gen_layout.addWidget(self.spin_density)
        gen_layout.addWidget(coords_group)
        gen_layout.addWidget(self.btn_generate)

        # --- алгоритм ---
        algo_group = QGroupBox("Алгоритм поиска", self)
        algo_layout = QVBoxLayout(algo_group)

        self.combo_algorithm = QComboBox(algo_group)
        # видимый текст + код для ядра
        self.combo_algorithm.addItem("A* (Chebyshev)", userData="astar")
        self.combo_algorithm.addItem("BFS", userData="bfs")
        self.combo_algorithm.addItem("Dijkstra", userData="dijkstra")

        algo_layout.addWidget(QLabel("Алгоритм:", algo_group))
        algo_layout.addWidget(self.combo_algorithm)

        # --- управление симуляцией ---
        sim_group = QGroupBox("Симуляция", self)
        sim_layout = QHBoxLayout(sim_group)

        self.btn_start = QPushButton("Старт", sim_group)
        self.btn_pause = QPushButton("Пауза", sim_group)
        self.btn_step = QPushButton("Шаг", sim_group)
        self.btn_reset = QPushButton("Сброс", sim_group)

        sim_layout.addWidget(self.btn_start)
        sim_layout.addWidget(self.btn_pause)
        sim_layout.addWidget(self.btn_step)
        sim_layout.addWidget(self.btn_reset)

        # --- скорость ---
        speed_group = QGroupBox("Скорость", self)
        speed_layout = QVBoxLayout(speed_group)

        self.slider_speed = QSlider(Qt.Orientation.Horizontal, speed_group)
        self.slider_speed.setRange(10, 1000)  # 10..1000 мс
        self.slider_speed.setValue(200)

        speed_layout.addWidget(QLabel("Задержка между шагами (мс):", speed_group))
        speed_layout.addWidget(self.slider_speed)

        self.label_speed_value = QLabel("0.200 s", speed_group)
        speed_layout.addWidget(self.label_speed_value)


        # собрать всё
        layout.addWidget(maze_group)
        layout.addWidget(gen_group)
        layout.addWidget(algo_group)
        layout.addWidget(sim_group)
        layout.addWidget(speed_group)
        layout.addStretch(1)

        self._connect_signals()

    def _connect_signals(self) -> None:
        # лабиринты
        self.combo_mazes.currentTextChanged.connect(self.maze_selected)
        self.btn_refresh.clicked.connect(self.refresh_requested)
        self.btn_delete.clicked.connect(self._on_delete_clicked)
        self.btn_import.clicked.connect(self.import_requested)

        # генерация
        self.btn_generate.clicked.connect(self._on_generate_clicked)

        # алгоритм
        self.combo_algorithm.currentIndexChanged.connect(self._on_algorithm_changed)

        # симуляция
        self.btn_start.clicked.connect(self.start_requested)
        self.btn_pause.clicked.connect(self.pause_requested)
        self.btn_step.clicked.connect(self.step_requested)
        self.btn_reset.clicked.connect(self.reset_requested)

        # скорость
        self.slider_speed.valueChanged.connect(self._on_speed_changed)

    # --- публичные методы для MainWindow ---

    def set_maze_names(self, names: list[str]) -> None:
        current = self.combo_mazes.currentText()
        self.combo_mazes.blockSignals(True)
        self.combo_mazes.clear()
        self.combo_mazes.addItems(names)
        # попытаться вернуть старый выбор
        if current and current in names:
            index = self.combo_mazes.findText(current)
            if index >= 0:
                self.combo_mazes.setCurrentIndex(index)
        self.combo_mazes.blockSignals(False)

    # --- приватные слоты / обработчики ---

    def _on_generate_clicked(self) -> None:
        name = self.edit_name.text().strip()
        if not name:
            return
        width = int(self.spin_width.value())
        height = int(self.spin_height.value())
        density = float(self.spin_density.value())

        self.generate_requested.emit(
            name, width, height, density,
            (self.spin_start_x.value(), self.spin_start_y.value()),
            (self.spin_finish_x.value(), self.spin_finish_y.value()),
        )

    def _on_delete_clicked(self) -> None:
        name = self.combo_mazes.currentText().strip()
        if not name:
            return
        self.delete_requested.emit(name)

    def _on_algorithm_changed(self, index: int) -> None:
        code = self.combo_algorithm.itemData(index)
        if not code:
            return
        self.algorithm_selected.emit(str(code))

    def _on_speed_changed(self, value: int):
        delay_seconds = max(0.0, float(value) / 1000.0)
        self.speed_changed.emit(delay_seconds)
        self.label_speed_value.setText(f"{delay_seconds:.3f} s")

