from .servo import BaseServo
from kosmo.audio.audio import AudioProcessor


class Mouth:
    yMin = -80
    yMax = 0

    def __init__(self, pin: int, yMin: float = yMin, yMax: float = yMax):
        self.y = BaseServo(pin, yMin, yMax)
        self.ap = AudioProcessor(self)

    def min(self):
        self.y.min()

    def max(self):
        self.y.max()

    def setY(self, angle: float):
        self.y.setPosition(angle)

    def getConfig(self):
        # A function that exposes all the values of the class, so the configuration can be saved and replicated
        return {'part': 'mouth', 'pin': self.y.pin, 'yMin': self.y.angMin, 'yMax': self.y.angMax}

    def getAngles(self):
        # Returns the angles of all servos for displaying on the dashboard
        return {'y': self.y.getAngle()}

    def speak(self, text, angry=False):
        self.ap.speak(text, angry)
