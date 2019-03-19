# THIS FILE IS NOT BEING USED FOR ANYTHING YET, BUT WILL BE FITTED TO WORK WITH THE REST OF THE PROGRAM LATER

import pyaudio
import wave
from audioop import rms
from kosmo.face import Mouth

class AudioProcessor:
    def __init__(self, filename, mouth: Mouth):
        self.CHUNK = 1024
        self.filename = filename
        self.deviation = 1000
        self.mouth = mouth

    def process(self):
        wf = wave.open(self.filename, 'rb')

        p = pyaudio.PyAudio()

        # open stream (2)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # read data
        data = wf.readframes(self.CHUNK)
        deviationValue = 1000

        howSoon = 3
        lastUpper = 0
        lastDowner = 0
        iteration = 0
        last = 0
        while len(data) > 0:
            iteration += 1
            stream.write(data)
            data = wf.readframes(self.CHUNK)
            rmsThing = rms(data, 2)
            if rmsThing > last + deviationValue and iteration - lastUpper > howSoon:
                lastUpper = iteration
                print('MIN')
                self.mouth.yMin()
            elif rmsThing < last - deviationValue and iteration - lastDowner > howSoon:
                lastDowner = iteration
                print('MAX')
                self.mouth.yMax()

            last = rmsThing
            print()

        # stop stream (4)
        stream.stop_stream()
        stream.close()

        # close PyAudio (5)
        p.terminate()