import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from sliderentrywidget import SliderEntryWidget

class VideoPlayerFrame(ttk.Frame):
    def __init__(self, parent, fps_max = 120):
        super().__init__(parent)
        self.cap = None
        self.fps_max = fps_max
        self.after_id = None

        self.canvas = tk.Canvas(self, width=800, height=800)
        self.canvas.grid(row=0, column=0, columnspan=2)

        ttk.Label(self, text="Playback Speed:").grid(row=1, column=0)

        self.playback_speed = SliderEntryWidget(self, initial_value=1.0, minmax=(1e-9, 2), clamp_int=False)
        self.playback_speed.grid(row=1, column=1)
        self.playback_speed.bind_on_change(self.update_playback_speed)

    def __del__(self):
        self.cap.release()

    def start_video(self, source):
        self.cap = cv2.VideoCapture(source)
        self.update_video()

    def stop_video(self):
        self.cap = None

    def update_playback_speed(self):
        if self.after_id: self.after_cancel(self.after_id)
        self.after_id = self.after(int(1e3 / (self.fps_max * self.playback_speed.get_value())), self.update_video)

    def update_video(self):
        if self.cap is None: return

        ret, frame = self.cap.read()
        if ret:
            frame_resized = cv2.resize(frame, (800, 800), interpolation=cv2.INTER_NEAREST)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)

            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.image = img_tk

        elif not ret and self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        
        self.after_id = self.after(int(1e3 / (self.fps_max * self.playback_speed.get_value())), self.update_video)