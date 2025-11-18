"""Алгоритм A* (заглушка)."""

import heapq
import itertools
import math

def chebyshev(a, b):
    return max(abs(a.x - b.x), abs(a.y - b.y))

class Astar():
    def __init__(self, maze, heruistic):
        self.maze = maze
        self.start = maze.start
        self.finish = maze.finish
        sx, sy = maze.start
        self.start_node = maze.grid[sy][sx]
        fx, fy = maze.finish
        self.finish_node = maze.grid[fy][fx]

        self.heruistic = heruistic

        self.counter = itertools.count(0)

        self.start_node.g = 0
        self.start_node.h = heruistic(self.start_node, self.finish_node)
        self.start_node.f = self.start_node.g + self.start_node.h

        self.open = []
        heapq.heappush(self.open, (self.start_node.f, self.start_node.h, next(self.counter), self.start_node))
        self.closed = set()
        self.current = None
        
        
    
    def get_current(self):
        while self.open:
            _, _, _, node = heapq.heappop(self.open)
            if node not in self.closed:
                return node
        return None

    def step(self):
        way = []
        current_node = self.get_current()
        self.current = current_node
        if current_node is None:
            return "NO_PATH", self.get_path(current_node)
        elif current_node is self.finish_node:
            return "PATH FOUND", self.get_path(current_node)
        self.closed.add(current_node)
        for neighbour_node in self.maze.get_neighbours(current_node.x, current_node.y):
            if neighbour_node in self.closed:
                continue
            length = math.sqrt(2) if (neighbour_node.x != current_node.x and neighbour_node.y != current_node.y) else 1
            temp_length = current_node.g + length
            if temp_length < neighbour_node.g:
                neighbour_node.g = temp_length
                neighbour_node.parent = current_node
                neighbour_node.h = self.heruistic(neighbour_node, self.finish_node)
                neighbour_node.f = neighbour_node.g + neighbour_node.h
                heapq.heappush(self.open, (neighbour_node.f, neighbour_node.h, next(self.counter), neighbour_node))
            else: continue
        return "IN PROCESS", self.get_path(current_node)
        
    def get_path(self, node):
        path = set()
        while node is not None:
            path.add((node.x, node.y))
            node = node.parent
        return path

    def _iter_open_nodes(self):
        for _, _, _, node in self.open:
            yield node

    def get_state(self):
        path = self.get_path(self.current) if self.current is not None else set()
        visited = {(n.x, n.y) for n in self.closed}
        frontier = {(n.x, n.y) for n in self._iter_open_nodes()}
        current = (self.current.x, self.current.y) if self.current is not None else None

        return {
            "path": path,
            "visited": visited,
            "frontier": frontier,
            "current": current,
        }