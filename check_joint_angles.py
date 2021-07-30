import evasdk

if __name__ == '__main__':
    IP = '172.16.16.2'
    TOKEN = '5930e264643dc3d4b4ff0ebb05da0ce404d3281a'
    robot = evasdk.Eva(IP, TOKEN)
    print(evasdk.__version__)
    print(robot.name()['name'])
    print(robot.versions())