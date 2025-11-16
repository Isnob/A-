"""Алгоритм A* (заглушка)."""

import yaml
import numpy as np

# TODO: реализовать эвристический поиск с манхэттенской метрикой или другой на выбор
# 1. Класс клетки сетки
# Это объект, который хранит всё, что нужно А* о конкретной точке.
# Что в нём должно быть по сути:
# координаты;
# можно ли по ней ходить;
# оценка накопленного пути;
# оценка расстояния до цели;
# итоговая оценка;
# ссылка на предыдущую клетку (для восстановления пути).
# Без этого алгоритм не сможет сравнивать варианты и не сможет потом собрать финальный маршрут.

# 2. Класс сетки
# Это полноценная структура, которая знает:
# размеры поля,
# все клетки,
# какие клетки соседи каких,
# какие клетки — стены,
# где старт и цель.
# Алгоритм должен обращаться к сетке, чтобы:
# получить соседей,
# проверить границы,
# узнать, свободна ли клетка.
# Если начнёшь писать А* без отдельного класса сетки — быстро запутаешься.

# 3. Класс самого алгоритма A*
# Это уже исполнитель:
# хранит список тех, кого нужно рассмотреть;
# хранит список тех, кто уже обработан;
# выполняет шаги алгоритма;
# управляет выбором лучшей клетки;
# вызывает сетку для получения соседей;
# формирует финальный путь.
# По факту — это «мотор», который работает на данных Grid и Node.



class Node():
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.walkable = type != "wall"
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')
        self.parent = None

class Grid():
    def __init__(self, data, maze):
        self.data = data[f"{maze}"]
        self.start = None
        self.finish = None
        self.grid = self._set_grid()
        self.width = len(self.data[0])
        self.length = len(self.data)

    def _set_grid(self):
        grid = []
        for y, row in enumerate(self.data):
            grid.append([])
            for x, ch in enumerate(row):
                if ch == "S":
                    node = Node(x, y, "start")
                    self.start = (x, y)
                elif ch == "F":
                    node = Node(x, y, "finish")
                    self.finish = (x, y)
                elif ch == 1:
                    node = Node(x, y, "wall")
                else:
                    node = Node(x, y, "empty")

                grid[y].append(node)

        return grid

    def get_neighbours(self, x, y):
        


data = yaml.safe_load(open("config/config.yaml")); 
maze = 'maze'

