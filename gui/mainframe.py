import tkinter
import time
from settings import Settings

class MainFrame(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        tkinter.Frame.__init__(self, master, *args, **kwargs)
        self.app_pointer = master
        self.color_manager = self.app_pointer.color_manager
        
        self.configure(bg=self.color_manager.background_color) #31,31,31
        self.canvas = tkinter.Canvas(master=self, bg=self.color_manager.background_color,
        highlightthickness=0, height=Settings.CANVAS_SIZE, width=Settings.CANVAS_SIZE)
