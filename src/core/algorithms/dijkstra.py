import heapq
import itertools
import math

class Dijkstra():
    def __init__(self, maze):
        self.maze = maze
        self.start = maze.start
        self.finish = maze.finish
        sx, sy = maze.start
        self.start_node = maze.grid[sy][sx]
        fx, fy = maze.finish
        self.finish_node = maze.grid[fy][fx]
        self.start_node.g = 0

        self.open = [[self.start_node.g, 0, self.start_node]]
        self.closed = set()
        
        self.counter = itertools.count(1)
    
    def get_current(self):
        while self.open:
            _, _, node = heapq.heappop(self.open)
            if node not in self.closed:
                return node
        return None

    def step(self):
        current = self.get_current()
        if current is None:
            return "NO_PATH", self.get_path(current)
        elif current is self.finish_node:
            return "PATH FOUND", self.get_path(current)
        self.closed.add(current)
        for neighbour_node in self.maze.get_neighbours(current.x, current.y):
            if neighbour_node in self.closed:
                continue
            length = math.sqrt(2) if (neighbour_node.x != current.x and neighbour_node.y != current.y) else 1
            temp_length = current.g + length
            if temp_length < neighbour_node.g:
                neighbour_node.g = temp_length
                neighbour_node.parent = current
                heapq.heappush(self.open, (neighbour_node.g, next(self.counter), neighbour_node))
            else: continue
        return "IN PROCESS", self.get_path(current)
        
    def get_path(self, node):
        path = set()
        while node is not None:
            path.add((node.x, node.y))
            node = node.parent
        return path
