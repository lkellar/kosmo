from .eye import Eye
from .mouth import Mouth
from .eyebrow import Eyebrow


class Face:
    # All the available parts
    leftEye, rightEye = None, None
    mouth = None
    leftEyebrow, rightEyebrow = None, None

    def addPart(self, config):
        part = config.pop('part')
        if part == "eye":
            self.addEye(**config)
        elif part == "mouth":
            self.addMouth(**config)
        elif part == "eyebrow":
            self.addEyebrow(**config)
        else:
            raise TypeError('Part type is invalid! Must be "eye", "mouth" or "eyebrow"')

    # Below are functions to add parts like Eyes or Mouths
    def addEye(self, side: str, xPin: int, yPin: int, xMin: float = Eye.xMin, xMax: float = Eye.xMax,
                 yMin: float = Eye.yMin, yMax: float = Eye.yMax):
        args = locals()
        del args['side']
        del args['self']
        if side == 'left':
            self.leftEye = Eye(**args)
        elif side == 'right':
            self.rightEye = Eye(**args)
        else:
            raise TypeError('Side must be "left" or "right"!')

    def addMouth(self, pin: int, yMin: float = Mouth.yMin, yMax: float = Mouth.yMax):
        args = locals()
        del args['self']
        self.mouth = Mouth(**args)

    def addEyebrow(self, side: str, pin: int, yMin: float = Eyebrow.yMin, yMax: float = Eyebrow.yMax):
        args = locals()
        del args['side']
        del args['self']
        if side == 'left':
            self.leftEyebrow = Eyebrow(**args)
        elif side == 'right':
            self.rightEyebrow = Eyebrow(**args)
        else:
            raise TypeError('Side must be "left" or "right"!')

    def fetchParts(self):
        # This function returns all the face parts that have been defined
        return vars(self)