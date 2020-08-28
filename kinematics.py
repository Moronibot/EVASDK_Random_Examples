import evasdk
from .robot_config import *


robot = evasdk.Eva(ip, token)

# This should be a position in the general working area
guess_position = [-0.0011505207512527704, 0.3263643682003021, -1.894236445426941,
                  0.002109288005158305, -1.5707484483718872, 0.004410329274833202]

with robot.lock():
    robot.control_go_to(guess_position)

# Grab the current joint angles
current_servo = robot.data_servo_positions()

# This will convert the servo angles to X-Y-Z and end effector coordinates
current_ik = robot.calc_forward_kinematics(current_servo)

print("Current servo angle position: {}".format(current_servo))
# Current servo angle position: [0.0018216577591374516, 0.32578912377357483, -1.894140601158142,
# 0.002109288005158305, -1.5700773000717163, 0.003739192383363843]

print("Current FK position: {}".format(current_ik))
# Current FK position: {'position': {'x': 0.34617966, 'y': 0.0008507436, 'z': 0.42513335}, 'orientation': {'w':
# 0.0015789923, 'x': 0.00095785555, 'y': 0.99999774, 'z': 0.0010590815}}

# The position coordinates are in METERS away from the robot
# The orientation values are QUATERNION

future_position = {'position': {'x': 0.3, 'y': 0, 'z': 0.3},
                   'orientation': {'w': 0, 'x': 0, 'y': 1, 'z': 0}}

future_position_1cm_X = {'position': {'x': 0.31, 'y': 0, 'z': 0.3},
                         'orientation': {'w': 0, 'x': 0, 'y': 1, 'z': 0}}

calculated_future_position = robot.calc_inverse_kinematics(guess_position, future_position['position'],
                                                           future_position['orientation'])

calculated_future_position_1cm_Z = robot.calc_inverse_kinematics(guess_position, future_position_1cm_X['position'],
                                                           future_position_1cm_X['orientation'])

print(calculated_future_position)
# {'ik': {'joints': [-3.436133e-08, 0.58707345, -2.4997797, -7.8321634e-08, -1.2288864, -5.9216084e-08],
# 'result': 'success'}}

print("Future FK position calc: {}".format(calculated_future_position['ik']['result']))
# Future FK position calc: success
# An unsuccessful IK calculation will return 'ik' in the result location

print("Future FK position: {}".format(calculated_future_position))
# Future FK position: {'ik': {'joints': [-3.436133e-08, 0.58707345, -2.4997797, -7.8321634e-08, -1.2288864,
# -5.9216084e-08], 'result': 'success'}}

if calculated_future_position['ik']['result'] == 'success':
    with robot.lock():
        print("Moving...")
        robot.control_go_to(calculated_future_position['ik']['joints'])
        print("Moving 1cm forward...")
        robot.control_go_to(calculated_future_position_1cm_Z['ik']['joints'])
if calculated_future_position['ik']['result'] == 'ik':
    print("Can't move there!")
