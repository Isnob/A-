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


class Maze():
    def __init__(self, data, name_maze):
        self.data = data[f"{name_maze}"]
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
                elif ch in (1, "1"):
                    node = Node(x, y, "wall")
                else:
                    node = Node(x, y, "empty")

                grid[y].append(node)

        return grid

    def get_neighbours(self, x, y, dim=8):

        if dim == 8:
            directions = [
                (0, 1),   # up
                (1, 0),   # right
                (0, -1),  # down
                (-1, 0),  # left
                (1, 1),   # up-right
                (1, -1),  # down-right
                (-1, -1), # down-left
                (-1, 1),  # up-left
            ]

        elif dim == 4:
            directions = [
                (0, 1),   # up
                (1, 0),   # right
                (0, -1),  # down
                (-1, 0),  # left
            ]

        neighbours = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.length:
                node = self.grid[ny][nx]
                if node.walkable:
                    neighbours.append(node)

        return neighbours
