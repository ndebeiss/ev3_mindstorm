import math

from Node import Node
from utils import print_maze, clear_maze
import heapq


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


def astar(maze, start, end, direction_list):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = set()

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list) 
    heapq.heappush(open_list, start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node)

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
            if maze[node_position[0]][node_position[1]].obstacle != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = heuristic(child.position, end_node.position)
            child.f = child.g + child.h

            # Child is already in the open list with a better g
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)
            maze[child.position[0]][child.position[1]].studied = 1
        #print_maze(maze)
    print("Couldn't get a path to destination")
    return None
    

    