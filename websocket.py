import evasdk
import socket
import json
import asyncio
import websockets
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import copy
import numpy as np
import math
import sys
import os
import yaml
from collections import deque

eva_ip = '192.168.1.245'
eva_token = '0268413f3efb10c74ba0f2e4a4cd78226b0d05cd'


def resolve_hostname():
    pass


def main():
    ROBOT_AXIS = 6
    '''
    config = load_yml('config')
    cfg = config['config']

    if not cfg['host_ip']:
        if cfg['host_domain']:
            try:
                cfg['host_ip'] = socket.gethostbyname(cfg['host_domain'])
                print(cfg['host_ip'])
            except:
                print('unable to obtain host ip')
        else:
            print('host_ip or host_domain required in yml')
'''
    tlock = threading.Lock()

    chart_data_x = [[s for s in range(1000)] for i in range(ROBOT_AXIS * 3)]
    chart_data_y = [[np.nan for s in range(1000)] for i in range(ROBOT_AXIS * 3)]

    ws_data = {
        'position': [[] for i in range(ROBOT_AXIS)],
        'current': [[] for i in range(ROBOT_AXIS)],
        'temp': [[] for i in range(ROBOT_AXIS)],
    }

    def chart():
        def data_generator():
            while True:
                with tlock:
                    for i in range(ROBOT_AXIS):
                        for x in ws_data['position'][i]:
                            chart_data_y[i].append(x)
                            chart_data_y[i].pop(0)

                        ws_data['position'][i].clear()

                        for x in ws_data['current'][i]:
                            chart_data_y[i + ROBOT_AXIS].append(x)
                            chart_data_y[i + ROBOT_AXIS].pop(0)

                        ws_data['current'][i].clear()

                        for x in ws_data['temp'][i]:
                            chart_data_y[i + (ROBOT_AXIS * 2)].append(x)
                            chart_data_y[i + (ROBOT_AXIS * 2)].pop(0)

                        ws_data['temp'][i].clear()

                yield chart_data_y

        def animate(plot_y):
            for i, line in enumerate(lines):
                line.set_ydata(plot_y[i])

            return lines

        ani = animation.FuncAnimation(fig, animate, data_generator, interval=1, blit=True)
        plt.show()

    # Standard plot
    # plt.ion()

    # General plot setup
    # host_ip = cfg['host_ip']
    host_ip = eva_ip
    # host_domain = cfg['host_domain']
    host_domain = socket.gethostbyaddr(eva_ip)[0]

    title = f'IP: {host_ip}, Domain: {host_domain}'

    fig, axs = plt.subplots(ncols=ROBOT_AXIS, nrows=3, figsize=(15, 5))
    plt.suptitle(title)

    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

    fig.subplots_adjust(left=0.05, right=0.9, hspace=0.5, wspace=0.5)
    lines = [[] for i in range(ROBOT_AXIS * 3)]

    for i, ax in enumerate(axs.flat):
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_xlim([0, 1000])

        if i < ROBOT_AXIS:
            title = f'Axis {i + 1}'
            ax.set_title(f'Axis {i}')
            ax.set_ylim([-3.14, 3.14])
            ax.set_ylabel('position')
        elif i < ROBOT_AXIS * 2:
            ax.set_ylim([0, 4000])
            ax.set_ylabel('current')
        else:
            ax.set_ylim([0, 7000])
            ax.set_ylabel('temp')

        lines[i], = ax.plot(chart_data_x[i], chart_data_y[i], 'b-')

    # ax1 = axs[0, 0]
    # ax1.spines['right'].set_visible(False)
    # ax1.spines['top'].set_visible(False)
    # ax1.set_ylim([-4, 4])
    # line1, = ax1.plot(chart_data_x[0], chart_data_y[0], 'b-')

    def io():
        async def eva_ws_example(host_ip, token):
            print('attempted to connect')
            websocket = await evasdk.ws_connect(host_ip, token)
            print('connected')

            time_since_msg = time.time()
            last_update = time.time()
            msg_count = 0

            while True:
                print('awaiting websockeet message')
                ws_msg_json = await websocket.recv()
                print('received websocket message')

                # print('WS msg delta T: {}, number: {}'.format(time.time() - time_since_msg, msg_count))
                msg_count += 1

                time_since_msg = time.time()

                ws_msg = json.loads(ws_msg_json)

                if 'changes' in ws_msg:

                    changes = ws_msg['changes']

                    # Multi threaded
                    with tlock:
                        if 'servos.telemetry.position' in changes:
                            for i in range(ROBOT_AXIS):
                                ws_data['position'][i].append(math.degrees(changes['servos.telemetry.position'][i]))
                                ws_data['current'][i].append(changes['servos.telemetry.current'][i])

                        if 'servos.telemetry.drive_temp' in changes:
                            for i in range(ROBOT_AXIS):
                                ws_data['temp'][i].append(changes['servos.telemetry.drive_temp'][i])

                        # Standard plot
                        # data_y.append(changes['servos.telemetry.position'][3])
                        # data_y.pop(0)
                        # line1.set_ydata(data_y)
                        # fig.canvas.draw()
                        # fig.canvas.flush_events()

                    # print(1/(time.time() - last_update))
                    last_update = time.time()

        loop = asyncio.new_event_loop()
        # loop.run_until_complete(eva_ws_example(eva_ip, eva_token))

    # Multi threading
    threading.Thread(target=io).start()
    # chart()

    # standard
    # while True:
    #     line1.set_ydata(data_y)
    #     fig.canvas.draw()
    #     fig.canvas.flush_events()
    #     time.sleep(0.1)


if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.join(root_dir, 'src'))
    sys.exit(main())