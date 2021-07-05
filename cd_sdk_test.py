"""
Collision Detection via API/SDK
Latest release now has collision detection however the API/SDK does not support it yet.
This is a temporary SDK option until the official SDK is updated.
"""
import json
from evasdk import Eva
from evasdk.eva_errors import eva_error


def collision_detection(on_off, setting):
    """ Temporary SDK option until the official SDK is updated """
    if setting not in ['low', 'medium', 'high']:
        eva_error('collision_detection error, no such sensitivity ' + setting)
    if on_off not in [True, False]:
        eva_error('collision_detection error, must be True/False')
    r = robot.api_call_with_auth('POST', 'controls/collision_detection',
                                 json.dumps({'enabled': on_off, 'sensitivity': setting}))
    if r.status_code != 200:
        eva_error('collision_detection error', r)


if __name__ == '__main__':
    IP = None
    TOKEN = None
    robot = Eva(IP, TOKEN)
    with robot.lock():
        collision_detection(True, 'medium')
