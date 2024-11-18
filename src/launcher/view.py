from tkinter import ttk
import numpy as np

from leniafunctions import create_kernel_2d, kernel_function, growth_function
from kernelsliderwidget import KernelSliderFrame
from growthsliderwidget import GrowthSliderFrame
from functionplotwidget import FunctionPlotFrame
from imageplotwidget import ImagePlotFrame
from videoplayer import VideoPlayerFrame

class View:
    def __init__(self, root):
        self.root = root
        self.root.title("Lenia Visualization")

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill='both', expand=True)

        # Create Settings
        self.settings_frame = ttk.Frame(self.main_frame)
        self.settings_frame.grid(row=0, column=0, sticky='nswe')

        self.plot_selector = ttk.Combobox(self.settings_frame, values=["Kernel 1D", "Kernel 2D", "Growth Function", "Video"], state="readonly")
        self.plot_selector.set("Kernel 1D") 
        self.plot_selector.grid(row=0, column=0, pady=(0, 20), columnspan=2, sticky='we')
        self.plot_selector.bind("<<ComboboxSelected>>", lambda *args: self.show_selected_plot())

        self.kernel_sliders = KernelSliderFrame(self.settings_frame)
        self.kernel_sliders.grid(row=1, column=0, columnspan=2, sticky='we')

        ttk.Separator(self.settings_frame, orient="horizontal").grid(row=2, column=0, columnspan=2, pady=20, sticky='we')

        self.growth_sliders = GrowthSliderFrame(self.settings_frame)
        self.growth_sliders.grid(row=3, column=0, columnspan=2, sticky='we')

        ttk.Separator(self.settings_frame, orient="horizontal").grid(row=4, column=0, columnspan=2, pady=20, sticky='we')

        ttk.Label(self.settings_frame, text="width", width=11).grid(row=5, column=0, padx=(0, 10), sticky="w")
        self.width_entry = ttk.Entry(self.settings_frame)
        self.width_entry.grid(row=5, column=1, sticky='we')
        self.width_entry.insert(0, "256")

        ttk.Label(self.settings_frame, text="height", width=11).grid(row=6, column=0, padx=(0, 10), sticky="w")
        self.height_entry = ttk.Entry(self.settings_frame)
        self.height_entry.grid(row=6, column=1, sticky='we')
        self.height_entry.insert(0, "256")

        ttk.Label(self.settings_frame, text="frame amount", width=11).grid(row=7, column=0, padx=(0, 10), sticky="w")
        self.frame_amount_entry = ttk.Entry(self.settings_frame)
        self.frame_amount_entry.grid(row=7, column=1, sticky='we')
        self.frame_amount_entry.insert(0, "1000")

        ttk.Label(self.settings_frame, text="iterations per frame", width=11).grid(row=8, column=0, padx=(0, 10), sticky="w")
        self.iteration_per_frame_entry = ttk.Entry(self.settings_frame)
        self.iteration_per_frame_entry.grid(row=8, column=1, sticky='we')
        self.iteration_per_frame_entry.insert(0, "1")

        ttk.Label(self.settings_frame, text="delta time", width=11).grid(row=9, column=0, padx=(0, 10), sticky="w")
        self.delta_time_entry = ttk.Entry(self.settings_frame)
        self.delta_time_entry.grid(row=9, column=1, sticky='we')
        self.delta_time_entry.insert(0, "1e-4")

        ttk.Label(self.settings_frame, text="blocks x", width=11).grid(row=10, column=0, padx=(0, 10), sticky="w")
        self.blocks_x_entry = ttk.Entry(self.settings_frame)
        self.blocks_x_entry.grid(row=10, column=1, sticky='we')
        self.blocks_x_entry.insert(0, "32")

        ttk.Label(self.settings_frame, text="blocks y", width=11).grid(row=11, column=0, padx=(0, 10), sticky="w")
        self.blocks_y_entry = ttk.Entry(self.settings_frame)
        self.blocks_y_entry.grid(row=11, column=1, sticky='we')
        self.blocks_y_entry.insert(0, "32")

        ttk.Label(self.settings_frame, text="threads x", width=11).grid(row=12, column=0, padx=(0, 10), sticky="w")
        self.threads_x_entry = ttk.Entry(self.settings_frame)
        self.threads_x_entry.grid(row=12, column=1, sticky='we')
        self.threads_x_entry.insert(0, "32")

        ttk.Label(self.settings_frame, text="threads y", width=11).grid(row=13, column=0, padx=(0, 10), sticky="w")
        self.threads_y_entry = ttk.Entry(self.settings_frame)
        self.threads_y_entry.grid(row=13, column=1, sticky='we')
        self.threads_y_entry.insert(0, "32")
        
        # Create Export
        self.export_frame = ttk.Frame(self.main_frame)
        self.export_frame.grid(row=1, column=0, sticky='swe')
        self.export_entry = ttk.Entry(self.export_frame)
        self.export_entry.grid(row=0, column=0, padx=(0, 5), sticky='we')
        self.export_entry.insert(0, "LeniaConfig")

        self.export_button= ttk.Button(self.export_frame, text="Export")
        self.export_button.grid(row=0, column=1)

        self.import_button= ttk.Button(self.export_frame, text="Import")
        self.import_button.grid(row=0, column=2)

        self.run_button= ttk.Button(self.export_frame, text="Run")
        self.run_button.grid(row=0, column=3)

        # Create Plots
        self.plot_frame = ttk.Frame(self.main_frame)
        self.plot_frame.grid(row=0, column=1, rowspan=2)

        self.kernel_plot = ImagePlotFrame(self.plot_frame, "Kernel 2D")
        self.kernel_slice = FunctionPlotFrame(self.plot_frame, "Kernel 1D", "", "")
        self.growth_plot = FunctionPlotFrame(self.plot_frame, "Growth Function", "Cell Value", "Growth Value")
        self.video_player = VideoPlayerFrame(self.plot_frame)

        # Stretching
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.export_frame.columnconfigure(0, weight=1)

        self.settings_frame.columnconfigure(1, weight=1)

        self.show_selected_plot()

    def show_selected_plot(self):
        selected_plot = self.plot_selector.get()
        
        self.kernel_plot.grid_forget()
        self.kernel_slice.grid_forget()
        self.growth_plot.grid_forget()
        self.video_player.grid_forget()
        self.video_player.stop_video()

        if   selected_plot == "Kernel 2D": self.kernel_plot.grid(row=0, column=0, padx=5, pady=5)
        elif selected_plot == "Kernel 1D": self.kernel_slice.grid(row=0, column=1, padx=5, pady=5)
        elif selected_plot == "Growth Function": self.growth_plot.grid(row=0, column=1, padx=5, pady=5)
        elif selected_plot == "Video": 
            self.video_player.grid(row=0, column=0, padx=5, pady=5)
            self.video_player.start_video("output/video.mp4")

    def update_kernel_plot(self, radius, peak_heights, alpha):
        self.kernel_plot.update_plot(create_kernel_2d(radius, peak_heights, alpha))

        x = np.linspace(-1, 1, 200)
        y = np.array([kernel_function(np.abs(value), peak_heights, alpha) for value in np.linspace(-1, 1, 200)])
        y = y / np.max(y)
        self.kernel_slice.update_plot(x, y)

    def update_growth_plot(self, mhu, sigma):
        x = np.linspace(0, 1, 200)
        self.growth_plot.update_plot(x, growth_function(x, mhu, sigma))
