import tkinter
from time import strftime
from settings import Settings

class MainFrame(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        tkinter.Frame.__init__(self, master, *args, **kwargs)
        self.app_pointer = master
        self.color_manager = self.app_pointer.color_manager
        
        self.configure(bg=self.color_manager.background_color) #31,31,31

        self.canvas = tkinter.Canvas(master=self, bg=self.color_manager.background_color,
        highlightthickness=0, height=Settings.CANVAS_SIZE, width=Settings.CANVAS_SIZE)
        self.canvas.place(anchor=tkinter.CENTER, relx=0.5, rely=0.5)

        self.fps_period_ms = int(1/Settings.FPS*1000)

        self.lbl = tkinter.Label(self, font = ('calibri', 40, 'bold'),
            background = 'purple',
            foreground = 'white')

        self.lbl.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def run(self):
        self.time()
        self.after(self.fps_period_ms, self.run)

    def time(self):
        string = strftime('%H:%M:%S %p')
        self.lbl.config(text = string)