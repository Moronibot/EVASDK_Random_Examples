#!/usr/bin/env python
"""
Opens a websocket and reads the frequency of data from the robot.
Using this to verify potential connectivity issues.
"""

from evasdk import *
from websockets import client
import time
import asyncio


class WebSocketStreamer:
    def __init__(self, ip, token, run_duration):
        self.IP = ip
        self.TOKEN = token
        self.RUN_DURATION = 60 * run_duration  # Mins
        self.CHECK_INTERVAL = 1  # Seconds
        self.results_list = []
        self.RUNNING = True

    def get_ws_token(self):
        http_client = EvaHTTPClient(self.IP, self.TOKEN)
        return http_client.auth_create_session()

    def write_to_log(self):
        with open("stream_log.csv", mode='w', newline='') as f:
            for entries in self.results_list:
                f.write(f'{entries[0]}, "{entries[1]}"\n')
        f.close()

    async def websocket_stream(self):
        stream = await ws_connect(self.IP, self.get_ws_token())
        start_time = time.time()
        while self.RUNNING:
            ws_msg_json = await stream.recv()
            self.results_list.append([time.time(), ws_msg_json])
            if time.time() > (start_time + self.RUN_DURATION):
                self.RUNNING = False
        print(f'{self.RUN_DURATION} seconds  = {len(self.results_list)}')
        print(f'Packets per seconds = {len(self.results_list) / self.RUN_DURATION}')
        self.write_to_log()

    def run(self):
        try:
            asyncio.get_event_loop().run_until_complete(self.websocket_stream())
        except:
            raise RuntimeError


if __name__ == '__main__':
    IP = ''
    TOKEN = ''

    ws_benchmark = WebSocketStreamer(IP, TOKEN, 0.1)
    ws_benchmark.run()
