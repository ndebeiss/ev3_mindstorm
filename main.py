#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
import utils
import algo
import math


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


# Write your program here.
ev3.speaker.beep()

infrared_sensor = InfraredSensor(Port.S4)
color_sensor = ColorSensor(Port.S2)
touch_sensor = TouchSensor(Port.S1)

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
midle_motor = Motor(Port.A)

# Initialize the drive base.
WHEEL_DIAMETER = 15
AXLE_TRACK = 102

drive_base = DriveBase(left_motor, right_motor, wheel_diameter=WHEEL_DIAMETER, axle_track=AXLE_TRACK)


MAX_X = 20
MAX_Y = 20
maze = [[algo.MazeNode() for _ in range(MAX_X)] for _ in range(MAX_Y)]

DIRECTION_LIST = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

DEST = (15, 15)
ORIGIN = (10, 10)
ORIGIN_DIRECTION = (1, 0)
TURN_STEPS = 8

actual_position = ORIGIN
actual_direction = ORIGIN_DIRECTION
best_path = algo.astar(maze, actual_position, DEST, DIRECTION_LIST)
while len(best_path) > 1:
    sensor_color = color_sensor.color()
    print ("colosensor:" + str(sensor_color))
    if sensor_color == Color.BLUE:
        midle_motor.run(200)
        ev3.speaker.say('blue')
    maze[actual_position[0]][actual_position[1]].chemin = 1
    print("best_path : " + str(best_path))
    best_direction = (best_path[1][0] - actual_position[0], best_path[1][1] - actual_position[1])
    print("best_direction : " + str(best_direction))
    index_of_actual_direction = utils.index_of_direction(DIRECTION_LIST, actual_direction)
    print("index_of_actual_direction : " + str(index_of_actual_direction))
    nb_steps = utils.get_nb_steps_to_direction(DIRECTION_LIST, best_direction, index_of_actual_direction, TURN_STEPS)
    print("nb_steps : " + str(nb_steps))

    while nb_steps != 0:
        distances = utils.turn_around(TURN_STEPS, nb_steps, drive_base, infrared_sensor)
        if distances[0] < 10:
            ev3.speaker.say('obstacle')
            # recule lègèrement
            drive_base.straight(-20)
        actual_direction = best_direction
        utils.mark_maze_obstacle(index_of_actual_direction, distances, actual_position, DIRECTION_LIST, maze)
        algo.print_maze(maze)
        index_of_actual_direction += nb_steps
        best_path = algo.astar(maze, actual_position, DEST, DIRECTION_LIST)
        best_direction = (best_path[1][0] - actual_position[0], best_path[1][1] - actual_position[1])
        print("best_direction : " + str(best_direction))
        nb_steps = utils.get_nb_steps_to_direction(DIRECTION_LIST, best_direction, index_of_actual_direction, TURN_STEPS)
        print("nb_steps : " + str(nb_steps))
    print("going forward")
    drive_base.straight(math.sqrt(actual_direction[0] ** 2 + actual_direction[1] ** 2) * 100)
    distances = utils.turn_around(TURN_STEPS, 0, drive_base, infrared_sensor)
    utils.mark_maze_obstacle(index_of_actual_direction, distances, actual_position, DIRECTION_LIST, maze)
    algo.print_maze(maze)
    actual_position = (actual_position[0] + actual_direction[0], actual_position[1] + actual_direction[1])
    print("actual_position : " + str(actual_position))
    best_path = algo.astar(maze, actual_position, DEST, DIRECTION_LIST)
