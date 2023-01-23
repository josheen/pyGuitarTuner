import tkinter
from settings import Settings
from audio_analyzer.pyaudio_impl import PitchDetect
import queue
import threading
from PIL import ImageTk, Image

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

        self.freq_lbl = tkinter.Label(self, font = ('calibri', 40, 'bold'),
            background = 'purple',
            foreground = 'white')

        self.freq_lbl.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)
        self.draw_moving_grid(0)

        self.note_lbl = tkinter.Label(self, font = ('calibri', 30, 'bold'),
            background = 'purple',
            foreground = 'white')

        self.note_lbl.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)

        self.currentPitch = 0
        self.currentNote = ["A", 4, 0]

        img = Image.open("gui/black-pointer.png")
        img = img.resize((30,30), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        self.tuner_pointer = tkinter.Label(self, image=img, bg=self.color_manager.background_color)
        self.tuner_pointer.image = img

        self.tuner_pointer.place(relx=0.5, rely=0.12, anchor=tkinter.CENTER)

        self.frequencyQueue = queue.Queue()
        self.pitchDetectionThread = PitchDetect(self.frequencyQueue)
        listenerThread = threading.Thread(target=self.listner, daemon=True)

        self.pitchDetectionThread.start()
        listenerThread.start()

    def run(self):
        self.update_label()
        self.after(self.fps_period_ms, self.run)

    def update_label(self):
        self.freq_lbl.config(text=self.currentPitch)
        self.note_lbl.config(text=self.currentNote)
        x_location = (self.currentNote[2]+100)/200
        self.tuner_pointer.place(relx=x_location, rely=0.12, anchor=tkinter.CENTER)

    def create_grid(self, entry_point):
        self.canvas.delete('grid_line') # Will only remove the grid_line
        # Creates all vertical lines
        for i in range(0, Settings.CANVAS_SIZE, Settings.GRID_SPACING):
            self.canvas.create_line([(i, 0), (i, Settings.CANVAS_SIZE)], tag='grid_line', fill=self.color_manager.grid_color)

        # Creates all horizontal lines
        for i in range(entry_point, Settings.CANVAS_SIZE, Settings.GRID_SPACING):
            self.canvas.create_line([(0, i), (Settings.CANVAS_SIZE, i)], tag='grid_line', fill=self.color_manager.grid_color)

    def draw_moving_grid(self, current_index):
        if current_index == Settings.GRID_SPACING:
            current_index = 0
        
        self.create_grid(current_index)
        current_index+=1
        self.after(75, self.draw_moving_grid, current_index)

    def listner(self):
        while True:
            if self.frequencyQueue:
                self.currentPitch = self.frequencyQueue.get()
                if self.currentPitch:
                    self.currentNote = self.pitchDetectionThread.cnvt_note(self.currentPitch)