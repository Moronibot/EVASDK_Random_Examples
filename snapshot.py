import evasdk

ip = '192.168.1.242'
token = '088de40da79d48183c5fc804cc97a1f4f130940b'

# Very simple script to grab a status snapshot from Eva
# The lock() is not required for grabbing snapshots

robot = evasdk.Eva(ip, token)

current_robot_status_json = robot.data_snapshot()

for nItem in current_robot_status_json:
    print(nItem)
    print(current_robot_status_json[nItem])
