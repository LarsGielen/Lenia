from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FunctionPlotFrame(ttk.Frame):
    def __init__(self, master, title, title_x, title_y):
        super().__init__(master)
        self.fig_growth, self.ax_growth = plt.subplots(figsize=(12, 6))  
        self.canvas_growth = FigureCanvasTkAgg(self.fig_growth, master=self)
        self.canvas_growth.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.title = title
        self.title_x = title_x
        self.title_y = title_y

    def update_plot(self, x, y):
        self.ax_growth.clear()
        self.ax_growth.plot(x, y)
        self.ax_growth.set_title(self.title)
        self.ax_growth.set_xlabel(self.title_x)
        self.ax_growth.set_ylabel(self.title_y)
        self.canvas_growth.draw()