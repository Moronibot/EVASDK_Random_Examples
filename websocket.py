import evasdk
import json
import asyncio
import time
from .robot_config import *

# This example shows usage of the eva_ws and eva_http modules, used for direct control
# using the network interfaces. eva_http also contains some helper functions not
# contained in the public API, such as lock_wait_for.

print('ip: [{}], token: [{}]\n'.format(ip, token))

http_client = evasdk.EvaHTTPClient(ip, token)

# The session token will be valid for 30 minutes, you'll need to renew the session
# if you want the websocket connection to continue after that point.
session_token = http_client.auth_create_session()

# Opened
# 1598543223.5871415
# Closed
# 1598545028.0620193

print("Websocket opened at {}".format(time.time()))

users = http_client.users_get()
print('Eva at {} users: {}\n'.format(host_ip, users))

joint_angles = http_client.data_servo_positions()
print('Eva current joint angles: {}'.format(joint_angles))


async def eva_ws_example(host_ip, session_token):
    websocket = await evasdk.ws_connect(host_ip, session_token)
    websocket_start_time = time.time()
    msg_count = 0
    time_since_msg = time.time()
    while True:
        websocket_running_time = time.time()
        try:
            ws_msg_json = await websocket.recv()
            # print('WS msg delta T: {}, number: {}'.format(time.time() - time_since_msg, msg_count))
            msg_count += 1
            time_since_msg = time.time()

            ws_msg = json.loads(ws_msg_json)
            # print(ws_msg['changes']['servos.telemetry.position'])
            timer = (websocket_running_time - websocket_start_time) / 60
            if round(timer, 4) % 2 == 0:
                print("Timer currently: {}".format(round(timer, 4)))
                print(ws_msg)
            elif timer >= 30:
                print("Restarted at {}".format(time.time()))
                websocket = await evasdk.ws_connect(host_ip, session_token)
                websocket_start_time = websocket_start_time + 1800
        except:
            print("Websocket unexpectedly closed at {}".format(time.time()))
            break


asyncio.get_event_loop().run_until_complete(eva_ws_example(host_ip, session_token))
