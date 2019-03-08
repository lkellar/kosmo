from .servo import BaseServo


class Eyebrow:
    yMin = 0
    yMax = 50
    # Again, the angMin and angMax have not been finalized

    def __init__(self, pin: int, yMin: float = yMin, yMax: float = yMax):
        self.y = BaseServo(pin, yMin, yMax)

    def min(self):
        self.y.min()

    def max(self):
        self.y.max()

    def setY(self, angle: float):
        self.y.setPosition(angle)
