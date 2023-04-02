class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
      self.parent = parent
      self.position = position

      self.g = 0
      self.h = 0
      self.f = 0

    def __eq__(self, other):
      return self.position == other.position
      
    def __hash__(self):
      return hash(self.position)

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f
