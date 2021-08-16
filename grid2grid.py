"""
Very, very, rough example of how to do grid_to_grid through the SDK.
Ideally, you would generate a complete toolpath and label that toolpath as "slot 1/10" or similar and change toolpaths
at the end of each pass. Using control_go_to() by itself and away from a toolpath does not allow for ease or alteration
nor does it allow you to use such features like pass-through or linear waypoints.
"""
from typing import List, Tuple, NamedTuple
import evasdk


class XYPoint(NamedTuple):
    x: float
    y: float


GridCorners = Tuple[XYPoint, XYPoint, XYPoint]


class Grid2D:
    """
    Grid2D is a iterable collection of XYPoints generated from a set of grid 
    corner positions and a number of rows and columns
    """

    def __init__(self, grid_corners: GridCorners, rows: int, columns: int):
        self.__current_position: int = 0
        self.__positions: List[XYPoint] = []

        x_start = grid_corners[0][0]
        x_end = grid_corners[1][0]

        y_start = grid_corners[1][1]
        y_end = grid_corners[2][1]

        column_step: float = (x_start - x_end) / (columns - 1)
        row_step: float = (y_start - y_end) / (rows - 1)

        for column in range(columns):
            for row in range(rows):
                x = x_start - (column_step * column)
                y = y_start - (row_step * row)
                self.__positions.append(XYPoint(x=x, y=y))

    def __iter__(self):
        return self

    def __next__(self) -> XYPoint:
        if self.__current_position > len(self.__positions) - 1:
            raise StopIteration
        else:
            next_position = self.__positions[self.__current_position]
            self.__current_position += 1
            return next_position

    def grid_len(self):
        return len(self.__positions)

    def get_n_position(self, n_slot):
        return self.__positions[n_slot]


class RobotFunctions:
    def __init__(self, robot_ob):
        self.robot = robot_ob

    def get_joint_angles(self, x_y_coords, z_coord, ee_orientation, pose_home):
        target_position = {'x': x_y_coords.x, 'y': x_y_coords.y, 'z': z_coord}
        position_joint_angles = self.robot.calc_inverse_kinematics(pose_home, target_position, ee_orientation)
        return position_joint_angles['ik']['joints']


if __name__ == '__main__':
    IP = None
    TOKEN = None
    eva = evasdk.Eva(IP, TOKEN)
    eva_funcs = RobotFunctions(eva)

    grid_1_corners: GridCorners = [
        XYPoint(x=0.20, y=0),
        XYPoint(x=0.40, y=0),
        XYPoint(x=0.40, y=0.4),
    ]
    grid_2_corners: GridCorners = [
        XYPoint(x=0.40, y=0),
        XYPoint(x=0.20, y=0),
        XYPoint(x=0.20, y=0.4),
    ]

    grid_common_z_position: float = 0.4

    grid_1 = Grid2D(grid_1_corners, rows=2, columns=4)
    grid_2 = Grid2D(grid_2_corners, rows=4, columns=2)

    end_effector_orientation = {'w': 0.0, 'x': 0.0, 'y': 1.0, 'z': 0.0}

    robot_home_pos = [0.057526037, 0.7658633, -1.9867575, 0.026749607, -1.732109, -0.011505207]

    with eva.lock():
        eva.control_go_to(robot_home_pos)
        for n_slot in range(grid_1.grid_len()):
            print(f"Moving from : {grid_1.get_n_position(n_slot)}")
            eva.control_go_to(eva_funcs.get_joint_angles(grid_1.get_n_position(n_slot), grid_common_z_position,
                                                         end_effector_orientation, robot_home_pos))
            print(f"Moving to : {grid_2.get_n_position(n_slot)}")
            eva.control_go_to(eva_funcs.get_joint_angles(grid_2.get_n_position(n_slot), grid_common_z_position,
                                                         end_effector_orientation, robot_home_pos))
        eva.control_go_to(robot_home_pos)
