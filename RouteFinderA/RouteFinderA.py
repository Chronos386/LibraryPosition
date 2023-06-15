import os
from queue import PriorityQueue


def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)


class RouteFinderA:
    def __init__(self):
        self.graph = []
        self.countPoints = 0
        self.filePath = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'files/graph.txt')

    def read_graph_from_file(self):
        self.graph = []
        with open(self.filePath, 'r') as file:
            for line in file:
                row = list(map(float, line.strip().split()))
                self.graph.append(row)

    def get_neighbors(self, current):
        neighbors = []
        for i in range(self.countPoints):
            if self.graph[current][i] != -1:
                neighbors.append(i)
        return neighbors

    def astar(self, start_point, end_point):
        came_from = {}
        cost_so_far = {start_point: 0}
        open_list = PriorityQueue()
        open_list.put((0, start_point))

        while not open_list.empty():
            _, current = open_list.get()

            if current == end_point:
                final_path = []
                while current in came_from:
                    final_path.append(current)
                    current = came_from[current]
                final_path.append(start_point)
                final_path.reverse()
                return final_path

            for next_ in self.get_neighbors(current):
                new_cost = cost_so_far[current] + self.graph[current][next_]
                if next_ not in cost_so_far or new_cost < cost_so_far[next_]:
                    cost_so_far[next_] = new_cost
                    priority = new_cost + heuristic((end_point, 0), (next_, 0))
                    open_list.put((priority, next_))
                    came_from[next_] = current
        return None

    def init_me(self):
        self.read_graph_from_file()
        self.countPoints = len(self.graph)

    def start(self, end_point):
        return self.astar(start_point=0, end_point=end_point)
