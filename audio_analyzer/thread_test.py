from pyaudio_impl import PitchDetect
import queue
import threading

q = queue.Queue()
p = PitchDetect(q)
p.start()

def client_thread():
    while True:
        if q:
            val = q.get()
            print("pitch: {}, queue size: {}".format(val, q.qsize()))
t = threading.Thread(target=client_thread)
t.start()