import evasdk

REGISTER_VALUE = True
IP = None
TOKEN = None
JOINTS = []

if __name__ == '__main__':
    robot = evasdk.Eva(IP, TOKEN)
    with robot.lock():
        robot.control_go_to(JOINTS)
        while robot.data_snapshot()['control']['state'] == 'running':
            if not REGISTER_VALUE:
                robot.control_pause()

