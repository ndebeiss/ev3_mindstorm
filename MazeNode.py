class MazeNode():
    """A cell of the maze """
    def __init__(self):
        self.obstacle = 0
        self.studied = 0
        self.visited = 0
        self.best_path = 0
        self.chemin = 0
        self.destination = 0

    def clear(self):
        self.studied = 0
        self.visited = 0
        self.best_path = 0
