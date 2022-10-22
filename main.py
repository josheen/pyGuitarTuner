import tkinter
import os
import time
import sys
import numpy as np
from gui.mainframe import MainFrame
from gui.colormanager import ColorManager

class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.color_manager = ColorManager()
        self.mainframe = MainFrame(self)
    def start(self):
        while True:
            self.update()
            time.sleep(1)

    def draw_main_frame(self):
        pass

if __name__ == "__main__":
    app = App()
    app.start()