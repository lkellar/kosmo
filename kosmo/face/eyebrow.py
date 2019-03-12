from .servo import BaseServo


class Eyebrow:
    yMin = 0
    yMax = 50
    # Again, the angMin and angMax have not been finalized

    def __init__(self, side: str, pin: int, yMin: float = yMin, yMax: float = yMax):
        self.y = BaseServo(pin, yMin, yMax)
        self.side = side

    def min(self):
        self.y.min()

    def max(self):
        self.y.max()

    def setY(self, angle: float):
        self.y.setPosition(angle)

    def getConfig(self):
        return {'side': self.side, 'part': 'eyebrow', 'pin': self.y.pin, 'yMin': self.y.angMin, 'yMax': self.y.angMax}