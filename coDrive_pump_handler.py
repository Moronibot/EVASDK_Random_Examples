"""
coDrive connected to an Eva with the following pinout:

coDrive     Eva Base IO
V IN - ->   Pin 1
V IN + ->   Pin 10
D1     ->   Pin 9
D2     ->   Pin 11
D3     ->   Pin 13
0V     ->   Pin 12
A      ->   Pin 17
AG     ->  Pin 24
"""

import evasdk
from time import sleep


class PumpHandler:
    """
    Pass Eva object to allow basic coDrive functionality.
    A lot of the __init__ could be passed as args when first initialising the class.
    """

    def __init__(self, eva_obj):
        self.robot = eva_obj
        self.ambient_pressure_voltage = 3  # Volts
        self.acceptable_suction_threshold = 2  # Volts
        self.acceptable_pressure_threshold = 5  # Volts
        self.pressure_pin = 'd0'  # Digital output 1
        self.vacuum_pin = 'd1'  # Digital output 2
        self.motor_pin = 'd2'  # Digital output 3
        self.tdx_pin = 'a0'  # Analog input 1
        self.wait_on_pump = 3  # Seconds

    def my_lock(self):
        """ Lock is required to toggle outputs """
        lock_call = self.robot.lock_status()
        if lock_call['owner'] == 'you' and lock_call['status'] == 'locked':
            return True
        else:
            return False

    def get_tdx_voltage(self):
        """ Returns the voltage at the pressure transducer rounded to 1 decimal place. """
        return round(self.robot.data_snapshot()['global.inputs'][self.tdx_pin], 1)

    def is_pressure_stable(self):
        """ Pressure is relative voltage above a certain level. """
        if self.get_tdx_voltage() < self.acceptable_pressure_threshold:
            return True
        else:
            return False

    def is_suction_stable(self):
        """ Suction is relative voltage below a certain level. """
        if self.get_tdx_voltage() > self.acceptable_suction_threshold:
            return True
        else:
            return False

    def is_pump_running(self):
        """ Checks the pin is set to active for running the pump. """
        if self.robot.gpio_get(self.motor_pin, 'output'):
            return True
        else:
            return False

    def suction_on(self):
        """
        Sets appropriate pins for suction mode and starts motor pump.
        Waits a set time for a vacuum to build.
        """
        if self.my_lock():
            self.robot.gpio_set(self.pressure_pin, False)
            self.robot.gpio_set(self.vacuum_pin, True)
            self.pump_run()
        sleep(self.wait_on_pump)
        if self.is_suction_stable():
            return True
        else:
            return False

    def suction_off(self):
        """ Toggles pin to off specified for suction mode and stops motor pump. """
        if self.my_lock():
            self.robot.gpio_set(self.vacuum_pin, False)
            self.pump_stop()

    def pressure_on(self):
        """
        Sets appropriate pins for pressure mode and starts motor pump.
        Waits a set time for pressure to build.
        """
        if self.my_lock():
            self.robot.gpio_set(self.vacuum_pin, False)
            self.robot.gpio_set(self.pressure_pin, True)
            self.pump_run()
        sleep(self.wait_on_pump)
        if self.is_pressure_stable():
            return True
        else:
            return False

    def pressure_off(self):
        """ Toggles pin to off specified for pressure mode and stops motor pump. """
        if self.my_lock():
            self.robot.gpio_set(self.pressure_pin, False)
            self.pump_stop()

    def pump_run(self):
        """ Toggles pin specified to run motor pump. """
        self.robot.gpio_set(self.motor_pin, True)

    def pump_stop(self):
        """ Toggles pin specified to run motor pump to off. """
        self.robot.gpio_set(self.motor_pin, False)


if __name__ == '__main__':
    # Todo input Eva IP and generate token before use
    IP = None
    TOKEN = None
    robot = evasdk.Eva(IP, TOKEN)
    codrive_unit = PumpHandler(robot)
    with robot.lock():
        print(codrive_unit.pressure_on())
        sleep(2)
        print(codrive_unit.suction_on())
        sleep(2)
        codrive_unit.suction_off()
