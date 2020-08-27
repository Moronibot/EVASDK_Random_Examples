import evasdk

# Very simple script to grab a status snapshot from Eva
# The lock() is not required for grabbing snapshots

token = ''
ip = ''

robot = evasdk.Eva(ip, token)

current_robot_status_json = robot.data_snapshot()

for nItem in current_robot_status_json:
    print(nItem)
    print(current_robot_status_json[nItem])