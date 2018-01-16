"""
Name: RPi Motor Controller
Project: ISS Pointer
Dev: DJGood
Date Created: Dec 16, 2017
Last Modfied: Dec 18, 2017

Dev: K4YT3X IZAYOI
Last Modified: Jan 15, 2018
"""
import RPi.GPIO as GPIO
from enum import Enum
from time import sleep
from exception import InvalidDirectionError


class DIRECTION(Enum):
    CW = 1
    CCW = 0


class Stepper(object):

    GEAR_RATIO = 2.5

    MICROSTEP_TRUTH_TABLE = {
        # resolution: (ms1, ms2)
        'full': (0, 0),
        'half': (1, 0),
        'quarter': (0, 1),
        'eigth': (1, 1)
    }

    MICROSTEP_RESOLUTION_MULTIPLIER = {
        'full': 1,
        'half': 0.5,
        'quarter': 0.25,
        'eigth': 0.125
    }

    def __init__(self, dir_pin, step_pin, ms1_pin, ms2_pin):
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.ms1_pin = ms1_pin
        self.ms2_pin = ms2_pin
        self.step_delay = 0.001
        self._microstep_resolution = 'full'
        self._direction = DIRECTION.CW
        self._azimuth = 0.0  # in degrees from true north

        self.setup()

    def __del__(self):
        self.teardown()

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        if isinstance(direction, DIRECTION):
            self._direction = direction
        else:
            raise InvalidDirectionError

    @property
    def microstep_resolution(self):
        return self._microstep_resolution

    @microstep_resolution.setter
    def microstep_resolution(self, resolution):
        if resolution not in self.MICROSTEP_TRUTH_TABLE.keys():
            self._microstep_resolution = 'eigth'
        else:
            self._microstep_resolution = resolution
        self.set_microstep_resolution_in_easydriver()

    @property
    def azimuth(self):
        return self._azimuth

    def set_microstep_resolution_in_easydriver(self):
        ms1, ms2 = self.MICROSTEP_TRUTH_TABLE[self._microstep_resolution]
        GPIO.output(self.ms1_pin, ms1)
        GPIO.output(self.ms2_pin, ms2)

    def setup(self):
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.ms1_pin, GPIO.OUT)
        GPIO.setup(self.ms2_pin, GPIO.OUT)

    def step(self):
        """
        Dev: DJGood
        Date Created: Dec 16, 2017
        Last Modfied: Dec 18, 2017

        Dev K4YT3X IZAYOI
        Last Modified: Jan 16, 2018

        Notes from DJGood: 0.9 degrees per step * resolution * gear_ratio
        This is probably the wrong way to do this but it works. It would be
        good to rethink how this could work.
        """
        degrees_moved = 0.9 * \
            self.MICROSTEP_RESOLUTION_MULTIPLIER[self._microstep_resolution] * \
            self.GEAR_RATIO
        if self._direction == DIRECTION.CCW:
            degrees_moved = -degrees_moved
        self._azimuth += degrees_moved
        GPIO.output(self.step_pin, 1)
        sleep(self.step_delay)
        GPIO.output(self.step_pin, 0)
        sleep(self.step_delay)

    def set_azimuth(self, angle):
        steps = angle * 2.5 * 10/9
        for _ in range(steps):
            self.step()


    def teardown(self):
        GPIO.cleanup()


if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    stepper = Stepper(12, 11, 13, 15)

