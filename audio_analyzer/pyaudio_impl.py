#! /usr/bin/env python

import pyaudio
import numpy as np
import aubio
import threading


class PitchDetect(threading.Thread):
    BUFFER_SIZE = 1024
    pyaudio_format = pyaudio.paFloat32
    n_channels = 1
    samplerate = 44100
    p_instance = pyaudio.PyAudio()

    tolerance = 0.8
    win_s = 4096 # fft size
    hop_s = BUFFER_SIZE # hop size
    pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
    pitch_o.set_unit("midi")
    pitch_o.set_tolerance(tolerance)

    def __init__(self, queue):
        super().__init__()
        self.running = False
        self.queue = queue
        try:
            self.stream = self.p_instance.open(
                                format=self.pyaudio_format,
                                channels=self.n_channels,
                                rate=self.samplerate,
                                input=True,
                                frames_per_buffer=self.BUFFER_SIZE)
        except Exception as e:
            print("Error with analyzer setup")
            raise;

    def run(self):
        self.running = True
        while True:
            try:
                audiobuffer = self.stream.read(self.BUFFER_SIZE)
                signal = np.fromstring(audiobuffer, dtype=np.float32)

                pitch = self.pitch_o(signal)[0]
                confidence = self.pitch_o.get_confidence()
                #print("{} / {}".format(pitch,confidence))

                self.queue.put(pitch)

            except KeyboardInterrupt:
                print("*** Ctrl+C pressed, exiting")
                break

        print("*** done recording")
        self.stream.stop_stream()
        self.stream.close()
        self.p_instance.terminate()
