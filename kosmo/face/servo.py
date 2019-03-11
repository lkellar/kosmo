from gpiozero import AngularServo
from time import sleep

from os import environ

class BaseServo:
    def __init__(self, pin: int, angMin: float = -90, angMax: float = 90):
        if environ['development'] == '1':
            # This creates a mock servo, for simulating controls and testing,
            # without having to use the Raspberry Pi every time
            self.s = DevAngularServo(pin, initial_angle=0)
        else:
            self.s = AngularServo(pin, initial_angle=0)
        self.angMax = angMax
        self.angMin = angMin

    def setPosition(self, angle: float):
        if angle > self.angMax or angle < self.angMin:
            raise ValueError('Angle out of range. Stay between {} and {}'.
                             format(self.angMin, self.angMax))

        self.s.angle = angle

    def max(self):
        self.s.angle = self.angMax

    def min(self):
        self.s.angle = self.angMin

    def mid(self):
        self.s.angle = (self.angMax + self.angMin) / 2

    def getAngle(self):
        return self.s.angle

    def calibrate(self):
        print('Moving to Zero')
        self.s.angle = 0
        sleep(1)
        self.s.angle = None
        print('Adjust the Motor so the Zero is proper')
        input()
        print('This is MAX')
        self.max()
        sleep(2)
        print(self.s.angle)
        print('\nTHIS IS MID')
        self.mid()
        sleep(2)
        print(self.s.angle)
        print('\nTHIS IS MIN')
        self.min()
        sleep(2)
        print(self.s.angle)
        print('\nTHIS IS ZERO')
        self.s.angle = 0
        sleep(2)


# A fake Angular Servo that doesn't actually connect to GPIO for testing purposes
class DevAngularServo:
    def __init__(self, pin: int, initial_angle: float = 0):
        self.pin = pin
        self.angle = initial_angle
