import tkinter
import os
import time
import sys
import numpy as np

class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.timer = 60
        self.label = tkinter.Label(text="")
        self.label.pack()

    def start(self):
        while True:
            self.update_clock()
            self.update()
            time.sleep(1)

    def update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)

if __name__ == "__main__":
    app = App()
    app.start()