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

        self.lbl.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)
        self.draw_moving_grid(0)

    def run(self):
        self.time()
        self.after(self.fps_period_ms, self.run)

    def time(self):
        string = strftime('%H:%M:%S %p')
        self.lbl.config(text = string)

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