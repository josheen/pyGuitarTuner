#! /usr/bin/env python

import pyaudio
import numpy as np
import aubio
import threading
import math

class PitchDetect(threading.Thread):
    BUFFER_SIZE = 1024
    PITCH_STANDARD = 440
    NOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    NUM_NOTES = 49
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

    def cnvt_note(self, freq):
        """
        Convert frequency to note, octave and cents
        """
        note_number = 12 * math.log2(freq/self.PITCH_STANDARD) + self.NUM_NOTES
        note_rounded = round(note_number)

        note = self.NOTES[(note_rounded - 1) % len(self.NOTES)]
        octave = (note_rounded + 8 ) // len(self.NOTES)

        nominal_freq = 2**((note_rounded-self.NUM_NOTES)/12)*self.PITCH_STANDARD
        cents = 1200*math.log2(freq/nominal_freq)
        return (note, octave, cents)

    def __init__(self, queue):
        super().__init__()
        self.daemon = True
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
            raise

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
