from tkinter import ttk, StringVar
from contextlib import suppress

class SliderEntryWidget(ttk.Frame):
    def __init__(self, parent, initial_value = 0, minmax = (0, 1), clamp_int = False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.clamp_int = clamp_int
        self.value = StringVar(value=initial_value)
        self.slider = ttk.Scale(self, length=200, from_=minmax[0], to=minmax[1], orient="horizontal")
        self.slider.grid(row=0, column=0, padx=(0, 10))
        self.slider.set(self.value.get())  
        self.entry = ttk.Entry(self, width=20, textvariable=self.value)
        self.entry.grid(row=0, column=1)
        self.value.trace_add("write", lambda *args: self.update_slider())
        self.slider.bind("<Motion>", lambda *args: self.update_value_from_slider())

    def update_slider(self):
        with suppress(ValueError): self.slider.set(int(round(float(self.value.get()))) if self.clamp_int else float(self.value.get())) 

    def update_value_from_slider(self):
        self.value.set(str(int(round(float(self.slider.get()))) if self.clamp_int else (float(self.slider.get()))))

    def bind_on_change(self, func):
        self.value.trace_add('write', lambda *args: func())

    def get_value(self):
        return int(round(float(self.slider.get()))) if self.clamp_int else (float(self.slider.get()))

    def set_value(self, value):
        self.value.set(value)