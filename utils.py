def turn_around(turn_step, nb_steps, drive_base, infrared_sensor):
    print("turning"+ str(nb_steps))
    returned = []
    angle = 0
    distance = infrared_sensor.distance()
    returned.append(distance)
    print('distance found at angle : ' + str(angle) + ' : ' + str(distance))
    for i in range(0, nb_steps):
        incr_angle = 360/turn_step
        angle += incr_angle
        drive_base.turn(incr_angle)
        distance = infrared_sensor.distance()
        print('distance found at angle : ' + str(angle) + ' : ' + str(distance))
        returned.append(distance)
    return returned


def index_of_direction(direction_list, direction):
    return next(i for i,v in enumerate(direction_list) if v[0] == direction[0] and v[1] == direction[1])

def get_nb_steps_to_direction(direction_list, best_direction, index_of_actual_direction, turn_steps):
    index_of_best_direction = index_of_direction(direction_list, best_direction)
    nb_steps = index_of_best_direction - index_of_actual_direction
    if nb_steps > turn_steps / 2:
        nb_steps -= turn_steps
    elif nb_steps < -turn_steps / 2:
        nb_steps += turn_steps
    return nb_steps

def mark_maze_obstacle(index_of_actual_direction, distances, actual_position, direction_list, maze):
    index_of_direction_distance = index_of_actual_direction
    for distance in distances:
        if distance < 40:
            studied_direction = direction_list[index_of_direction_distance]
            print("marking studied_direction : " + str(studied_direction) + " as obstacle")
            x_studied = actual_position[0] + studied_direction[0]
            y_studied = actual_position[1] + studied_direction[1]
            actual_cell = maze[x_studied][y_studied]
            print("marking cell : " + str((x_studied, y_studied)) + " as obstacle")
            actual_cell.obstacle = 1
        index_of_direction_distance = (index_of_direction_distance + 1) % 8
