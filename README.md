# Kosmo
An animatronic face controlled via servos and a Raspberry Pi

## Installation
For development, clone the repository and install dependencies via pipenv

`pipenv install`

This project runs on python3.5, because the Raspberry Pi doesn't play well with newer versions.

## Face Sub-Library

The Face (`kosmo/face/`) module is currently the only way to control the face. 

A Face instance takes in part parameters as an input, and creates new parts that can be controlled. See example below

```
f = Face()

f.addEye('left', 2, 3)
f.addEye('right', 20, 21, yMax=90)

brow = {'part': 'eyebrow', 'side': 'left', 'yPin': 7}

f.addPart(brow)
f.addEyebrow('right', 8)

f.addMouth(10, yMin=0)
```

### kosmo.Face()
Parameters: None

Once parts are added, they can be referenced via the following variables
* `leftEye`
* `rightEye`
* `mouth`
* `leftEyebrow`
* `rightEyebrow`

### addPart()
Adds a part to the Face. Good for programmatically adding parts.

Required Parameters:
* `config` (dict): A dictionary of parameters for one of the other Add functions, plus a "type" of part. See example below.
Acceptable "types" are "eye", "mouth", and "eyebrow"
```json
{
    "part": "eye",
    "side": "right",
    "xPin": 20,
    "yPin": 21,
    "yMax": 90
  }
```

### addEye()
Adds an [Eye](#eye) instance to the Face

Required Parameters:
* `side` (string): Designates which eye to be controlled. Only "left" or "right" is a valid parameter.
* `xPin` (int): The GPIO pin where the servo controlling the X axis resides.
* `yPin` (int): The GPIO pin where the servo controlling the Y axis resides.

Optional Parameters:
* `xMin` (float): The minimum angle of the X Axis
* `xMax` (float): The maximum angle of the X Axis
* `yMin` (float): The minimum angle of the Y Axis
* `yMax` (float): the minimum angle of the Y Axis


### addMouth()
Adds a [Mouth](#mouth) instance to the Face

Required Parameters:
* `pin` (int): The GPIO pin where the servo controlling the mouth resides

Optional Parameters:
* `yMin` (float): The minimum angle of the Y Axis
* `yMax` (float): The maximum angle of the Y Axis


### addEyebrow()
Adds a [Eyebrow](#eyebrow) instance to the Face


Required Parameters:
* `side` (string): Designates which eyebrow to be controlled. Only "left" or "right" is a valid parameter.
* `pin` (int): The GPIO pin where the servo controlling the eyebrow resides.

Optional Parameters:
* `yMin` (float): The minimum angle of the Y Axis
* `yMax` (float): The maximum angle of the Y Axis

## Face Part Classes

### Eye

Required Parameters:
* `side` (string): Designates which eye to be controlled. Only "left" or "right" is a valid parameter.
* `xPin` (int): The GPIO pin where the servo controlling the X axis resides.
* `yPin` (int): The GPIO pin where the servo controlling the Y axis resides.

Optional Parameters:
* `xMin` (float): The minimum angle of the X Axis
* `xMax` (float): The maximum angle of the X Axis
* `yMin` (float): The minimum angle of the Y Axis
* `yMax` (float): the minimum angle of the Y Axis

Available Functions:
* `setX(angle: float)`: Pass a float between the xMin and xMax to set the X angle.
* `setY(angle: float)`: Pass a float between the yMin and yMax to set the Y angle.
* `x.max() or y.max()`: Sets the corresponding servo's angle to the maximum.
* `x.min() or y.min()`: Sets the corresponding servo's angle to the mid point.
* `x.mid() or y.mid()`: Sets the corresponding servo's angle to the midpoint.

####Mouth

Required Parameters:
* `pin` (int): The GPIO pin where the servo controlling the mouth resides.

Optional Parameters:
* `yMin` (float): The minimum angle of the Y Axis
* `yMax` (float): The maximum angle of the Y Axis

Available Functions:
* `open()`: Opens the mouth servo to the maximum angle
* `close()`: Closes the mouth servo to the minimum angle
* `setY(angle: float)`: Pass a float between yMin and yMax to set the Y angle

### Eyebrow

Required Parameters:
* `side` (string): Designates which eyebrow to be controlled. Only "left" or "right" is a valid parameter.
* `pin` (int): The GPIO pin where the servo controlling the eyebrow resides.

Optional Parameters:
* `yMin` (float): The minimum angle of the Y Axis
* `yMax` (float): The maximum angle of the Y Axis

Available Functions:
* `max()`: Sets the eyebrow servo to the maximum angle
* `min()`: Sets the eyebrow servo to the minimum angle
* `setY(angle: float)` Pass a float between yMin and yMax to set the Y angle.

## Servo Calibration
Any servo motor can be directly accessed via syntax like `myFace.leftEye.x` or `myFace.mouth.y`

All servo motors have a calibrate function, which moves the servo to the zero position, and waits for a person to externally tune the servo. It then cycles through Max angle, Mid angle, Min angle, and Zero again.
