import evasdk
import json

with open('config.json') as f:
    cfg = json.load(f)

robot = evasdk.Eva(cfg['ip'], cfg['token'])

# Changes can only be carried out with the robot lock.
with robot.lock():

    # Simply sets the digital output 0 to True
    robot.gpio_set('d0', True)

    # {'d0': True, 'd1': False, 'd2': False, 'd3': False, 'ee_d0': False, 'ee_d1': False}
    print(robot.data_snapshot()['global.outputs'])
