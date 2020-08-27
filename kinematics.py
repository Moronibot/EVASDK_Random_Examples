import evasdk
from math import radians

ip = '192.168.1.242'
token = '088de40da79d48183c5fc804cc97a1f4f130940b'

robot = evasdk.Eva(ip, token)

guess_position = [-0.0011505207512527704, 0.3263643682003021, -1.894236445426941,
                  0.002109288005158305, -1.5707484483718872, 0.004410329274833202]

with robot.lock():
    robot.control_go_to(guess_position)

current_servo = robot.data_servo_positions()
current_ik = robot.calc_forward_kinematics(current_servo)

print("Current servo angle position: {}".format(current_servo))
print("Current FK position: {}".format(current_ik))

future_position = {'position': {'x': 0.3, 'y': 0, 'z': 0.3},
                   'orientation': {'w': 0, 'x': 0, 'y': 1, 'z': 0}}

error_position = {'position': {'x': 0.25820893, 'y': -0.00024254227, 'z': 0.36010402},
                  'orientation': {'w': 0, 'x': 0, 'y': 1, 'z': 0}}

calculated_future_position = robot.calc_inverse_kinematics(guess_position, future_position['position'],
                                                           future_position['orientation'])

print(calculated_future_position)
print("Future FK position calc: {}".format(calculated_future_position['ik']['result']))
print("Future FK position: {}".format(calculated_future_position))

if calculated_future_position['ik']['result'] == 'success':
    with robot.lock():
        print("Moving")
        robot.control_go_to(calculated_future_position['ik']['joints'])
if calculated_future_position['ik']['result'] == 'ik':
    print("Can't move there!")
