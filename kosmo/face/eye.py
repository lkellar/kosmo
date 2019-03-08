from .servo import BaseServo


class Eye:
    xMin = -50
    xMax = 50
    yMin = -90
    yMax = 50
    # The yMin and yMax haven't been finalized, the 50s are just place holders

    def __init__(self, xPin: int, yPin: int, xMin: float = xMin, xMax: float = xMax,
                 yMin: float = yMin, yMax: float = yMax):
        self.x = BaseServo(xPin, xMin, xMax)
        self.y = BaseServo(yPin, yMin, yMax)

    def setX(self, angle: float):
        self.x.setPosition(angle)

    def setY(self, angle: float):
        self.y.setPosition(angle)