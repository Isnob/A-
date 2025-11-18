from collections import deque

class BFS():
    def __init__(self, maze):
        self.maze = maze
        self.start = maze.start
        self.finish = maze.finish
        sx, sy = maze.start
        self.start_node = maze.grid[sy][sx]
        fx, fy = maze.finish
        self.finish_node = maze.grid[fy][fx]
        
        self.open = deque()
        self.open.append(self.start_node)
        self.closed = set()
        self.current = None

    def step(self):
        if not self.open:
            if self.current:
                return "NO_PATH", self.get_path(self.current)
            return "NO_PATH", set()

        self.current = self.open.popleft()
        current = self.current

        if current is self.finish_node:
            return "PATH FOUND", self.get_path(current)

        self.closed.add(current)
        neighbours = self.maze.get_neighbours(current.x, current.y, dim=4)
        for neighbour in neighbours:
            if neighbour in self.closed or neighbour in self.open:
                continue
            neighbour.parent = current
            self.open.append(neighbour)
        return "IN PROCESS", self.get_path(current)

    def get_path(self, node):
        path = set()
        while node is not None:
            path.add((node.x, node.y))
            node = node.parent
        return path
