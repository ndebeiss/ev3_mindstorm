from MazeNode import MazeNode
import algo

def test_astar():
    MAX_X = 20
    MAX_Y = 20
    maze = [[MazeNode() for _ in range(MAX_Y)] for _ in range(MAX_X)]
    DIRECTION_LIST = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    DEST = (15, 15)
    ORIGIN = (5, 5)
    print("Testing A star algorithm")
    best_path = algo.astar(maze, ORIGIN, DEST, DIRECTION_LIST)
    print(str(best_path))


def test_astar_obstacle():
    MAX_X = 20
    MAX_Y = 20
    maze = [[MazeNode() for _ in range(MAX_Y)] for _ in range(MAX_X)]
    maze[10][10].obstacle = 1
    DIRECTION_LIST = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    DEST = (15, 15)
    ORIGIN = (5, 5)
    print("Testing A star algorithm")
    best_path = algo.astar(maze, ORIGIN, DEST, DIRECTION_LIST)
    print(str(best_path))

def test_astar_wall():
    MAX_X = 20
    MAX_Y = 20
    maze = [[MazeNode() for _ in range(MAX_Y)] for _ in range(MAX_X)]
    for y in range(9,15):
        maze[10][y].obstacle = 1
    DIRECTION_LIST = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    DEST = (15, 15)
    ORIGIN = (5, 5)
    print("Testing A star algorithm")
    best_path = algo.astar(maze, ORIGIN, DEST, DIRECTION_LIST)
    print(str(best_path))


def test_astar_two_wall():
    MAX_X = 20
    MAX_Y = 20
    maze = [[MazeNode() for _ in range(MAX_Y)] for _ in range(MAX_X)]
    for y in range(7,14):
        maze[10][y].obstacle = 1
    maze[10][14].obstacle = 1
    maze[9][14].obstacle = 1
    DIRECTION_LIST = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    DEST = (15, 15)
    maze[DEST[0]][DEST[1]].destination = 1
    ORIGIN = (5, 5)
    print("Testing A star algorithm")
    best_path = algo.astar(maze, ORIGIN, DEST, DIRECTION_LIST)
    assert best_path is not None
    print(str(best_path))
    print("longueur du chemin : " + str(len(best_path)))

