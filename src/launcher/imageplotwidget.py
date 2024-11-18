from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ImagePlotFrame(ttk.Frame):
    def __init__(self, master, title):
        super().__init__(master)
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.title = title

    def update_plot(self, image):
        self.ax.clear()
        self.ax.imshow(image, cmap='viridis', interpolation='nearest')
        self.ax.set_title(self.title)
        self.canvas.draw()