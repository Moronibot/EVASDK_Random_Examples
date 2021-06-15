#!/usr/bin/env python
"""
Basic electrical switch connected to Eva which is monitored while a toolpath is run.
You will need to upload a valid toolpath before running this script.
"""
import evasdk

# Todo input Eva IP and generate token before use
IP = None
TOKEN = None

robot = evasdk.Eva(IP, TOKEN)


def stop_button_monitor():
    """ Monitors the digital input 0 pin for any state change. """
    while robot.data_snapshot()['control']['state'] == 'running':
        GLOBAL_FLAG = robot.data_snapshot()['global.inputs']['d0']
        if GLOBAL_FLAG:
            with robot.lock():
                robot.control_pause()


def robot_state_handler():
    """ Catches the robot in either state which is suitable to restart the toolpath from. """
    ROBOT_STATE = robot.data_snapshot()['control']['state']
    GLOBAL_FLAG = robot.data_snapshot()['global.inputs']['d0']
    if ROBOT_STATE == 'ready' and not GLOBAL_FLAG:
        with robot.lock():
            robot.control_home()
            robot.control_run(loop=1, wait_for_ready=False, mode='automatic')
        stop_button_monitor()
    elif ROBOT_STATE == 'paused' and not GLOBAL_FLAG:
        with robot.lock():
            robot.control_cancel()
            robot.control_home()


if __name__ == '__main__':
    while True:
        robot_state_handler()
