import pyaudio
import wave
from audioop import rms
import subprocess
from io import BytesIO


class AudioProcessor:
    def __init__(self, mouth):
        self.CHUNK = 256
        self.mouth = mouth
        self.p = pyaudio.PyAudio()

    def speak(self, text, french=False):
        # Main entry point for speech commands,
        # picks an english-us voice, unless french=True, then the spooky french voice
        voice = 'en-french' if french else 'english-us'
        # generate an espeak wav of the text provided
        wav = self.generate(text, voice)
        # Play the audio and move the mouth
        self.process(wav)

    def generate(self, text, voice='english-us'):
        cmd = ['espeak', '--stdout', '-v', voice, text]
        # Passes some text to be turned into wav by espeak
        return BytesIO(subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE).stdout)

    def process(self, wav):
        # turn the bytes into a wav object
        wf = wave.open(wav)

        # open stream (2)
        stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        # read data
        data = wf.readframes(self.CHUNK)

        # The LIMIT is the rms number where if the rms is above the Limit, the mouth opens, rms is below, mouth closes
        LIMIT = 2000
        # The STAGGER delays the audio playing so that the mouth can open before the speaking starts
        STAGGER = 4
        staggerList = []
        iteration = 0
        mouthOpen = False

        while len(data) > 0:
            iteration += 1
            data = wf.readframes(self.CHUNK)
            # find the RMS
            rmsThing = rms(data, 2)
            if rmsThing > LIMIT and not mouthOpen:
                self.mouth.min()
                mouthOpen = True
            elif rmsThing < LIMIT and mouthOpen:
                self.mouth.max()
                mouthOpen = False

            # put the data in the stagger list to be played later
            staggerList.insert(0, data)
            if len(staggerList) == STAGGER:
                stream.write(staggerList.pop())

        # play the rest of the audio
        for i in staggerList:
            stream.write(i)

        # stop stream (4)
        stream.stop_stream()
        stream.close()
