# THIS FILE IS NOT BEING USED FOR ANYTHING YET, BUT WILL BE FITTED TO WORK WITH THE REST OF THE PROGRAM LATER

import pyaudio
from sys import argv
import wave
from audioop import rms
from gpiozero import AngularServo

s = AngularServo(2)

CHUNK = 1024

if len(argv) < 2:
    print('Plays a wave file.\n\nUsage: {} filename.wav'.format(argv[0]))
    exit(1)

file = argv[1]

wf = wave.open(file, 'rb')

p = pyaudio.PyAudio()

# open stream (2)
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# read data
data = wf.readframes(CHUNK)

# listo = []

# play stream (3)

uppers = []
downers = []
num = 0

last = 0
lastUpper = 0
lastDowner = 0

saves = []

deviationValue = 1000
howSoon = 3
while len(data) > 0:
    num += 1
    stream.write(data)
    data = wf.readframes(CHUNK)
    rmsThing = rms(data, 2)
    print(rmsThing)
    # listo.append(rmsThing)
    if rmsThing > last + deviationValue and num - lastUpper <= howSoon:
        saves.append((num, 'UPPER'))
    if rmsThing < last - deviationValue and num - lastDowner <= howSoon:
        saves.append((num, 'DOWNR'))

    if rmsThing > last + deviationValue and num - lastUpper > howSoon:
        lastUpper = num
        uppers.append((num, last, rmsThing))
        s.angle = -90
    elif rmsThing < last - deviationValue and num - lastDowner > howSoon:
        lastDowner = num
        downers.append((num, last, rmsThing))
        s.angle = 90

    last = rmsThing
    print()

# stop stream (4)
stream.stop_stream()
stream.close()

# close PyAudio (5)
p.terminate()

print('These are the uppers')
print(uppers)
print(len(uppers))
print()
print('These are the downers')
print(downers)
print(len(downers))

print('These are the saves')
print(saves)
print(len(saves))