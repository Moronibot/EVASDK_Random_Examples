#!/usr/bin/env python
"""
Basic electrical switch connected to Eva which is monitored while a toolpath is run.
You will need to upload a valid toolpath before running this script.
"""
import evasdk


class RunAndPause:
    def __init__(self, robot_ip, robot_token):
        self.eva = evasdk.Eva(robot_ip, robot_token)

    def stop_button_monitor(self):
        """ Monitors the digital input 0 pin for any state change. """
        while self.eva.data_snapshot()['control']['state'] == 'running':
            button_pin = self.eva.data_snapshot()['global.inputs']['d0']
            if button_pin:
                with self.eva.lock():
                    self.eva.control_pause()

    def robot_state_handler(self):
        """ Catches the robot in either state which is suitable to restart the toolpath from. """
        snapshot = self.eva.data_snapshot()
        robot_state = snapshot['control']['state']
        button_active = snapshot['global.inputs']['d0']
        if robot_state == 'ready' and not button_active:
            with self.eva.lock():
                self.eva.control_home()
                self.eva.control_run(loop=0, wait_for_ready=False, mode='automatic')
            self.stop_button_monitor()
        elif robot_state == 'paused' and not button_active:
            with self.eva.lock():
                self.eva.control_cancel()
                self.eva.control_home()

    def run(self):
        """ Main running loop """
        try:
            while True:
                self.robot_state_handler()
        except KeyboardInterrupt:
            with self.eva.lock():
                self.eva.control_stop_loop(wait_for_ready=False)
            quit()


if __name__ == '__main__':
    IP = None
    TOKEN = None
    app = RunAndPause(IP, TOKEN)
    app.run()
