#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase

from MazeNode import MazeNode
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
maze = [[MazeNode() for _ in range(MAX_X)] for _ in range(MAX_Y)]

DIRECTION_LIST = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]

DEST = (15, 15)
maze[DEST[0]][DEST[1]].destination = 1
ORIGIN = (5, 5)
ORIGIN_DIRECTION = (1, 0)
TURN_STEPS = 8

actual_position = ORIGIN
actual_direction = ORIGIN_DIRECTION

ev3.speaker.say("For my master nicolas debeissat, i will go from start " + str(ORIGIN) + " to destination " + str(DEST))

best_path = algo.astar(maze, actual_position, DEST, DIRECTION_LIST)
print("best_path : " + str(best_path))
while len(best_path) > 1:
    sensor_color = color_sensor.color()
    print ("sensor_color:" + str(sensor_color))
    if sensor_color is not None:
        ev3.speaker.say("enemy of color " + str(sensor_color))
        midle_motor.run_angle(1000, 1000)
    best_direction = (best_path[1][0] - actual_position[0], best_path[1][1] - actual_position[1])
    print("best_direction : " + str(best_direction))
    index_of_actual_direction = utils.index_of_direction(DIRECTION_LIST, actual_direction)
    print("index_of_actual_direction : " + str(index_of_actual_direction))
    nb_steps = utils.get_nb_steps_to_direction(DIRECTION_LIST, best_direction, index_of_actual_direction, TURN_STEPS)
    print("nb_steps : " + str(nb_steps))

    while nb_steps != 0:
        ev3.speaker.say("turning " + str(nb_steps) +  " steps")
        distances = utils.turn_around(TURN_STEPS, nb_steps, drive_base, infrared_sensor, index_of_actual_direction, actual_position, DIRECTION_LIST, maze)
        actual_direction = best_direction
        if distances[-1] < 40:
            ev3.speaker.say('obstacle')
            # recule lègèrement
            drive_base.straight(-20)
        index_of_actual_direction += nb_steps
        best_path = algo.astar(maze, actual_position, DEST, DIRECTION_LIST)
        print("best_path : " + str(best_path) + " from actual_position : " + str(actual_position))
        best_direction = (best_path[1][0] - actual_position[0], best_path[1][1] - actual_position[1])
        print("best_direction : " + str(best_direction))
        nb_steps = utils.get_nb_steps_to_direction(DIRECTION_LIST, best_direction, index_of_actual_direction, TURN_STEPS)
        print("nb_steps : " + str(nb_steps))
    print("going forward")
    ev3.speaker.say('going forward')
    drive_base.straight(math.sqrt(actual_direction[0] ** 2 + actual_direction[1] ** 2) * 100)
    actual_position = (actual_position[0] + actual_direction[0], actual_position[1] + actual_direction[1])
    maze[actual_position[0]][actual_position[1]].chemin = 1
    print("actual_position : " + str(actual_position))
    if nb_steps != 0:
        ev3.speaker.say("turning " + str(nb_steps) +  " steps")
    distances = utils.turn_around(TURN_STEPS, nb_steps, drive_base, infrared_sensor, index_of_actual_direction, actual_position, DIRECTION_LIST, maze)
    actual_direction = best_direction
    print("actual_direction : " + str(actual_direction))
    if distances[0] < 40:
        ev3.speaker.say('obstacle')
        # recule lègèrement
        drive_base.straight(-20)
    best_path = algo.astar(maze, actual_position, DEST, DIRECTION_LIST)
    print("best_path : " + str(best_path) + " from actual_position : " + str(actual_position))

ev3.speaker.say("succeed arriving at destination " + str(DEST) + ", thank you giving me life nicolas debeissat")
