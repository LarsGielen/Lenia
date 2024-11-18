from tkinter import ttk, StringVar
from sliderentrywidget import SliderEntryWidget

class KernelSliderFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        ttk.Label(self, text="radius").grid(row=0, column=0, sticky="w")
        self.radius_slider = SliderEntryWidget(self, initial_value=18, minmax=(1, 100), clamp_int=True)
        self.radius_slider.grid(row=0, column=1, sticky='w')

        ttk.Label(self, text="alpha").grid(row=1, column=0, sticky="w")
        self.alpha_slider = SliderEntryWidget(self, initial_value=4, minmax=(1, 10), clamp_int=False)
        self.alpha_slider.grid(row=1, column=1, sticky='w')

        self.peak_heights = StringVar(value="1")
        ttk.Label(self, text="peak heights").grid(row=3, column=0, sticky='w')
        self.entry = ttk.Entry(self, width=5, textvariable=self.peak_heights)
        self.entry.grid(row=3, column=1, sticky='ew')

        self.columnconfigure(0, weight=1, minsize=110)

    def bind_on_change(self, func):
        self.radius_slider.bind_on_change(func)
        self.alpha_slider.bind_on_change(func)

    def get_values(self):
        peak_heights = [float(x.strip()) for x in self.peak_heights.get().split(',')]

        return self.radius_slider.get_value(), peak_heights, self.alpha_slider.get_value() 

    def set_values(self, radius, alpha, peak_heights):
        self.radius_slider.set_value(radius)
        self.alpha_slider.set_value(alpha)

        self.peak_heights.set(str(peak_heights).replace('[', '').replace(']', ''))