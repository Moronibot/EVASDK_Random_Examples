import evasdk
import json

with open('config.json') as f:
    cfg = json.load(f)

robot = evasdk.Eva(cfg['ip'], cfg['token'])

# Create a linear toolpath between two points and save it to the current directory

blank_toolpath = {
    "metadata": {},
    "timeline": {},
    "waypoints": {},
}

left_position = {'position': {'x': 0.3, 'y': 0, 'z': 0.3},
                 'orientation': {'w': 0, 'x': 0, 'y': 1, 'z': 0}}

right_position = {'position': {'x': 0.3, 'y': 0, 'z': 0.3},
                  'orientation': {'w': 0, 'x': 0, 'y': 1, 'z': 0}}
