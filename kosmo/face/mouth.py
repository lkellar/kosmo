from .servo import BaseServo


class Mouth:
    yMin = 0
    yMax = 50

    # The AngMin and AngMax have not been finalized, just placeholders
    def __init__(self, pin: int, yMin: float = yMin, yMax: float = yMax):
        self.y = BaseServo(pin, yMin, yMax)

    def close(self):
        self.y.min()

    def open(self):
        self.y.max()

    def setY(self, angle: float):
        self.y.setPosition(angle)

    def getConfig(self):
        return {'part': 'mouth', 'pin': self.y.pin, 'yMin': self.yMin, 'yMax': self.yMax}
