# THIS FILE IS NOT BEING USED FOR ANYTHING YET, BUT WILL BE FITTED TO WORK WITH THE REST OF THE PROGRAM LATER

import pyaudio
import wave
from audioop import rms
from . import _espeak

class AudioProcessor:
    def __init__(self, mouth):
        self.CHUNK = 1024
        self.deviation = 1000
        self.mouth = mouth

        rate =_espeak.Initialize(_espeak.AUDIO_OUTPUT_RETRIEVAL, 1000)
        if rate == -1:
            raise RuntimeError("Couldn't initialize espeak")

        _espeak.SetSynthCallback(self.process)

        text = 'This is a test sentence'
        _espeak.Synth(text, flags=_espeak.ENDPAUSE)

    def process(self, wav, numsample, events):
        print()
        print(type(wav))
        print()
        print(numsample)
        print()
        print(events)
        print()
        wf = wave.open(wav)

        p = pyaudio.PyAudio()

        # open stream (2)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=_espeak.RATE,
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