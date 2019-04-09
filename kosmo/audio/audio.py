import pyaudio
import wave
from audioop import rms
import subprocess
from io import BytesIO


class AudioProcessor:
    def __init__(self, mouth):
        self.CHUNK = 256
        self.mouth = mouth

    def speak(self, text, angry=False):
        voice = 'en-french' if angry else 'english-us'
        wav = self.generate(text, voice)
        self.process(wav)

    def generate(self, text, voice='english-us'):
        cmd = ['espeak', '--stdout', '-v', voice, text]
        return BytesIO(subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE).stdout)

    def process(self, wav):
        wf = wave.open(wav)

        p = pyaudio.PyAudio()

        # open stream (2)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # read data
        data = wf.readframes(self.CHUNK)

        LIMIT = 2000
        STAGGER = 4
        staggerList = []
        iteration = 0
        mouthOpen = False

        while len(data) > 0:
            iteration += 1
            data = wf.readframes(self.CHUNK)
            rmsThing = rms(data, 2)
            if rmsThing > LIMIT and not mouthOpen:
                self.mouth.min()
                mouthOpen = True
            elif rmsThing < LIMIT and mouthOpen:
                self.mouth.max()
                mouthOpen = False

            staggerList.insert(0, data)
            if len(staggerList) == STAGGER:
                stream.write(staggerList.pop())

        for i in staggerList:
            stream.write(i)

        # stop stream (4)
        stream.stop_stream()
        stream.close()

        # close PyAudio (5)
        p.terminate()
