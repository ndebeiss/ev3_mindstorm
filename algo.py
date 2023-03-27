import math

def heuristic(position, dest):
    return math.sqrt((dest[0] - position[0]) ** 2 + (dest[1] - position[1]) ** 2)


def reconstruct_path(current_node, maze):
    path = []
    current = current_node
    while current is not None:
        maze[current.position[0]][current.position[1]].best_path = 1
        path.append(current.position)
        current = current.parent
    print_maze(maze)
    return path[::-1] # Return reversed path


def get_max_x(maze):
    return len(maze) - 1


def get_max_y(maze):
    return len(maze[len(maze) - 1])


def print_maze(maze):
    print(" ", end='')
    for x in range(0, get_max_x(maze)):
        print("-", end='')
    print("")
    for y in range(0, get_max_y(maze)):
        print("|", end='')
        for x in range(0, get_max_x(maze)):
            if maze[x][y].chemin == 1:
                print('C', end='')
            elif maze[x][y].best_path == 1:
                print('B', end='')
            elif maze[x][y].obstacle == 1:
                print('X', end='')
            elif maze[x][y].visited == 1:
                print('V', end='')
            elif maze[x][y].studied == 1:
                print('S', end='')
            else:
                print(' ', end='')
        print("|")
    print(" ", end='')
    for x in range(0, get_max_x(maze)):
        print("-", end='')
    print("")

def clear_maze(maze):
    for x in range(0, get_max_x(maze)):
        for y in range(0, get_max_y(maze)):
            maze[x][y].studied = 0
            maze[x][y].visited = 0
            maze[x][y].best_path = 0


class MazeNode():
    """A cell of the maze """
    def __init__(self):
        self.obstacle = 0
        self.studied = 0
        self.visited = 0
        self.best_path = 0
        self.chemin = 0

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


def astar(maze, start, end, direction_list):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    print("clearing maze")
    clear_maze(maze)

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        maze[current_node.position[0]][current_node.position[1]].visited = 1
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            return reconstruct_path(current_node, maze)

        # Generate children
        children = []
        for new_position in direction_list: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            #print ("pourquoi il n' a pas trouvé l'obstacle ?"+ str(maze[node_position[0]][node_position[1]].obstacle))
            if maze[node_position[0]][node_position[1]].obstacle != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = heuristic(child.position, end_node.position)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
            maze[child.position[0]][child.position[1]].studied = 1
        print_maze(maze)
    

    