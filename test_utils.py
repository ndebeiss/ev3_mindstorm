import pytest

import MazeNode
import algo
import utils

TURN_STEPS = 8
DIRECTION_LIST = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
MAX_X = 20
MAX_Y = 20
maze = [[MazeNode.MazeNode() for _ in range(MAX_X)] for _ in range(MAX_Y)]


def test_index_of_direction():
    assert utils.index_of_direction(DIRECTION_LIST, (1, 1)) == 7
    assert utils.index_of_direction(DIRECTION_LIST, (0, -1)) == 0

def test_get_nb_steps_to_direction():
    assert utils.get_nb_steps_to_direction(DIRECTION_LIST, (1, 1), 7, TURN_STEPS) == 0
    assert utils.get_nb_steps_to_direction(DIRECTION_LIST, (1, 1), 0, TURN_STEPS) == -1
    assert utils.get_nb_steps_to_direction(DIRECTION_LIST, (0, 1), 0, TURN_STEPS) == 1
    assert utils.get_nb_steps_to_direction(DIRECTION_LIST, (-1, -1), 5, TURN_STEPS) == -1
    assert utils.get_nb_steps_to_direction(DIRECTION_LIST, (0, 1), 7, TURN_STEPS) == 2


def test_mark_maze_obstacle():
    actual_position = (5, 5)
    maze[actual_position[0]][actual_position[1]].visited = 1
    utils.print_maze(maze)
    utils.mark_maze_obstacle(4, [100,0,100,100,100,100,100,0], actual_position, DIRECTION_LIST, maze)
    assert maze[0][0].obstacle == 0
    assert maze[5][5].obstacle == 0
    assert maze[6][6].obstacle == 0
    assert maze[4][6].obstacle == 1
    assert maze[6][5].obstacle == 1
    utils.print_maze(maze)

def test_mark_maze_front_obstacle():
    actual_position = (8, 8)
    maze[actual_position[0]][actual_position[1]].visited = 1
    utils.print_maze(maze)
    utils.mark_maze_obstacle(0, [0,100,100,100,100,100,100,100], actual_position, DIRECTION_LIST, maze)
    utils.print_maze(maze)
    assert maze[8][8].obstacle == 0
    assert maze[9][8].obstacle == 0
    assert maze[9][9].obstacle == 0
    assert maze[8][9].obstacle == 0
    assert maze[7][9].obstacle == 0
    assert maze[7][8].obstacle == 0
    assert maze[7][7].obstacle == 0
    assert maze[8][7].obstacle == 1


def test_mark_maze_all_obstacle():
    actual_position = (10, 10)
    maze[actual_position[0]][actual_position[1]].visited = 1
    utils.print_maze(maze)
    utils.mark_maze_obstacle(4, [0,0,0,0,0,0,0,0], actual_position, DIRECTION_LIST, maze)
    assert maze[0][0].obstacle == 0
    assert maze[10][10].obstacle == 0
    assert maze[9][9].obstacle == 1
    assert maze[10][9].obstacle == 1
    assert maze[9][10].obstacle == 1
    utils.print_maze(maze)


if __name__ == "__main__":
    test_index_of_direction()
    test_get_nb_steps_to_direction()
    test_mark_maze_obstacle()
    