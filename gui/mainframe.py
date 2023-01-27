import tkinter
from settings import Settings
from audio_analyzer.pyaudio_impl import PitchDetect
import queue
import threading
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class MainFrame(tkinter.Frame):
    MAX_X_DATA_SAMPLES = 100
    MAX_Y_DATA_SAMPLES = 100
    def __init__(self, master, *args, **kwargs):
        tkinter.Frame.__init__(self, master, *args, **kwargs)
        self.app_pointer = master
        self.color_manager = self.app_pointer.color_manager
        
        self.configure(bg=self.color_manager.background_color) #31,31,31

        self.fps_period_ms = int(1/Settings.FPS*1000)

        self.canvas = tkinter.Canvas(master=self, bg=self.color_manager.background_color,
        highlightthickness=0, height=Settings.CANVAS_SIZE, width=Settings.CANVAS_SIZE)
        self.canvas.place(anchor=tkinter.CENTER, relx=0.5, rely=0.5)


        self.figure = Figure(figsize=(4,5), dpi=100)
        self.figure.patch.set_facecolor(self.color_manager.background_color)
        self.ax = self.figure.add_subplot(111)
        self.figure.tight_layout()
        self.ax.grid()
        self.ax.set_facecolor(self.color_manager.background_color)

        self.x_data = [0]
        self.y_data = [0]

        self.plot = self.ax.plot(self.x_data, self.y_data)[0]

        self.ax.set_ylim(-100, 100)
        self.ax.set_xlim(0, 100)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        self.currentPitch = 0
        self.currentNote = ["A", 4, 0]

        img = Image.open("gui/black-pointer.png")
        img = img.resize((30,30), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        self.tuner_pointer = tkinter.Label(self, image=img, bg=self.color_manager.background_color)
        self.tuner_pointer.image = img

        self.freq_lbl = tkinter.Label(self, font = ('calibri', 40, 'bold'),
            background = self.color_manager.background_color,
            foreground = 'white')

        self.freq_lbl.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.note_lbl = tkinter.Label(self, font = ('calibri', 30, 'bold'),
            background = self.color_manager.background_color,
            foreground = 'white')

        self.note_lbl.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

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

        if len(self.x_data) >= self.MAX_X_DATA_SAMPLES:
            pass
        else:
            self.x_data.append(self.x_data[-1]+1)

        if self.currentPitch:
            x_location = (self.currentNote[2]+100)/200
            self.y_data.insert(0,self.currentNote[2])
        else:
            x_location = 0.5
            self.y_data.insert(0,0)

        self.tuner_pointer.place(relx=x_location, rely=0.06, anchor=tkinter.CENTER)

        if len(self.y_data) > self.MAX_Y_DATA_SAMPLES:
            self.y_data = self.y_data[:self.MAX_Y_DATA_SAMPLES]

        self.plot.set_xdata(self.x_data)
        self.plot.set_ydata(self.y_data)
        self.canvas.draw_idle()


    def listner(self):
        while True:
            if self.frequencyQueue:
                self.currentPitch = self.frequencyQueue.get()
                if self.currentPitch:
                    self.currentNote = self.pitchDetectionThread.cnvt_note(self.currentPitch)