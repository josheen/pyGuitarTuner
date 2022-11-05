import tkinter
import os
import time
import sys
import numpy as np
from gui.mainframe import MainFrame
from gui.colormanager import ColorManager
from settings import Settings

class App(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.color_manager = ColorManager()
        self.mainframe = MainFrame(self)
        self.mainframe.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.minsize(Settings.WIDTH, Settings.HEIGHT)
        self.resizable(False, False)
    def start(self):
        self.draw_main_frame()
        self.mainloop()

    def draw_main_frame(self):
        self.mainframe.run()

if __name__ == "__main__":
    app = App()
    app.start()