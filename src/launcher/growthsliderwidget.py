from tkinter import ttk
from sliderentrywidget import SliderEntryWidget

class GrowthSliderFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        ttk.Label(self, text="mhu").grid(row=0, column=0, sticky="w")
        self.mhu_slider = SliderEntryWidget(self, initial_value=0.14, minmax=(0, 1), clamp_int=False)
        self.mhu_slider.grid(row=0, column=1, sticky='w')

        ttk.Label(self, text="sigma").grid(row=1, column=0, sticky="w")
        self.sigma_slider = SliderEntryWidget(self, initial_value=0.015, minmax=(0.01, 0.2), clamp_int=False)
        self.sigma_slider.grid(row=1, column=1, sticky='w')

        self.columnconfigure(0, weight=1, minsize=110)

    def bind_on_change(self, func):
        self.mhu_slider.bind_on_change(func)
        self.sigma_slider.bind_on_change(func)

    def get_values(self):
        return self.mhu_slider.get_value(), self.sigma_slider.get_value() 

    def set_values(self, mhu, sigma):
        self.mhu_slider.set_value(mhu)
        self.sigma_slider.set_value(sigma)