#!/usr/bin/env python
"""
Basic script demonstrating how to use the wait_for_ready flag alongside functions
such as control_pause().
"""
import time
import evasdk

if __name__ == '__main__':
    IP = None
    TOKEN = None
    robot = evasdk.Eva(IP, TOKEN)
    current_joints = [0.004506206139922142, 0.8510977029800415, -2.4415009021759033, -0.0033556853886693716, -1.5967310667037964, 0.00038350690738298]
    future_joints = [0.004122699145227671, 0.8507142066955566, -2.439870834350586, -0.002013411372900009, -1.598169207572937, 3.1068854331970215]
    print(robot.data_snapshot()['control']['state'])
    with robot.lock():
        robot.control_go_to(current_joints)
        # To use the wait_for_ready=False you need to be in automatic mode as teach will not allow this for safety reason
        robot.control_go_to(future_joints, wait_for_ready=False, mode='automatic')
        print(f"Joints before pause: {robot.data_servo_positions()}")
        time.sleep(1)
        robot.control_pause()
        print(robot.data_snapshot()['control']['state'])
        # This should display an axis 6 position that is not exactly
        print(f"Joints after pause: {robot.data_servo_positions()}")
        print(f"Joints expected if not paused: {future_joints}")
