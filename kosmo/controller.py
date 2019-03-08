from .face import Face
import json
from os import path
from time import sleep

currentDir = path.dirname(path.realpath(__file__))

with open(path.join(currentDir, '../', 'config.json'), 'r') as f:
    config = json.load(f)

f = Face()

for i in config:
    f.addPart(i)

# Below is just some demo stuff, to be removed later

f.leftEye.x.calibrate()
f.rightEye.x.calibrate()

while True:
    f.leftEye.x.max()
    f.rightEye.x.max()
    sleep(1)
    f.leftEye.y.min()
    f.rightEye.y.max()
    sleep(1)
    f.leftEye.x.min()
    f.rightEye.x.min()
    sleep(1)
    f.leftEye.y.max()
    f.rightEye.y.min()
    sleep(1)
