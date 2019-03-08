from gpiozero import AngularServo
from time import sleep


class BaseServo:
    def __init__(self, pin: int, angMin: float = -90, angMax: float = 90):
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
        self.s.mid()

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

