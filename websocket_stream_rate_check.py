#!/usr/bin/env python
"""
Opens a websocket and reads the frequency of data from the robot.
Using this to verify potential connectivity issues.
"""

from evasdk import *
import time
import asyncio
import matplotlib.pyplot
import json
import csv


class LiveDataGrapher:
    def __init__(self, file):
        self.file = open(file, mode='r')

    def graph_it(self):
        pass


class WebSocketStreamer:
    def __init__(self, ip, token, run_duration=20):
        self.IP = ip
        self.TOKEN = token
        self.RUN_DURATION = 60 * run_duration  # Mins
        self.CHECK_INTERVAL = 1  # Seconds
        self.results_list = []
        self.RUNNING = True

    def write_to_log(self):
        with open("stream_log.csv", mode='w', newline='') as f:
            for entries in self.results_list:
                f.write(f'{entries[0]}, "{entries[1]}"\n')
        f.close()

    async def websocket_stream(self):
        stream = await ws_connect(self.IP, self.TOKEN)
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
    IP = '10.10.60.175'
    TOKEN = '4182f0358d31b004953305474dab53d8e5e764a2'

    #graph_it = LiveDataGrapher("stream_log.txt")
    ws_benchmark = WebSocketStreamer(IP, TOKEN, 0.1)
    ws_benchmark.run()
