import tkinter as tk
from view import View
import json
import subprocess

class Controller:
    def __init__(self, root):
        self.view = View(root)

        self.view.kernel_sliders.bind_on_change(self.on_kernel_change)
        self.view.growth_sliders.bind_on_change(self.on_growth_change)
        self.view.export_button.bind("<Button-1>", self.export_lenia)
        self.view.import_button.bind("<Button-1>", lambda *args: self.import_lenia(self.view.export_entry.get()))
        self.view.run_button.bind("<Button-1>", self.run_lenia)

    def on_kernel_change(self):
        radius, peak_heights, alpha = self.view.kernel_sliders.get_values()
        self.view.update_kernel_plot(radius, peak_heights, alpha)

    def on_growth_change(self, *args):
        mhu, sigma = self.view.growth_sliders.get_values()
        self.view.update_growth_plot(mhu, sigma)

    def export_lenia(self, *args):
        export_name = self.view.export_entry.get()

        frame_width = self.view.width_entry.get()
        frame_height = self.view.height_entry.get()
        frame_amount = self.view.frame_amount_entry.get()
        iteration_per_frame = self.view.iteration_per_frame_entry.get()

        blocks_x = self.view.blocks_x_entry.get()
        blocks_y = self.view.blocks_y_entry.get()
        threads_x = self.view.threads_x_entry.get()
        threads_y = self.view.threads_y_entry.get()

        delta_time = self.view.delta_time_entry.get()
        radius, peak_heights, alpha = self.view.kernel_sliders.get_values()
        mhu, sigma = self.view.growth_sliders.get_values()

        data = {
            "frameWidth": int(frame_width),
            "frameHeight": int(frame_height),
            "frameAmount": int(frame_amount),
            "iteration_per_frame": int(iteration_per_frame),
            "deltaTime": float(delta_time),
            "kernel_radius": int(radius),
            "kernel_alpha": int(alpha),
            "kernel_peak_heights": peak_heights,
            "growth_mhu": float(mhu),
            "growth_sigma": float(sigma),
            "blocks_x": int(blocks_x),
            "blocks_y": int(blocks_y),
            "threads_x": int(threads_x),
            "threads_y": int(threads_y),
        }

        with open(export_name + ".json", 'w') as file:
            json.dump(data, file, indent=4)

    def import_lenia(self, file, *args):
        with open(file + ".json", 'r') as file: data = json.load(file)

        self.view.width_entry.delete(0, tk.END)
        self.view.width_entry.insert(0, data["frameWidth"])

        self.view.height_entry.delete(0, tk.END)
        self.view.height_entry.insert(0, data["frameHeight"])

        self.view.frame_amount_entry.delete(0, tk.END)
        self.view.frame_amount_entry.insert(0, data["frameAmount"])

        self.view.delta_time_entry.delete(0, tk.END)
        self.view.delta_time_entry.insert(0, data["deltaTime"])

        self.view.kernel_sliders.set_values(
            data["kernel_radius"],
            data["kernel_alpha"],
            data["kernel_peak_heights"]
        )

        # Update growth sliders
        self.view.growth_sliders.set_values(
            data["growth_mhu"],
            data["growth_sigma"]
        )

    def run_lenia(self, *args):
        self.export_lenia()
        subprocess.run(
            ["bash", "./run_lenia.bash"], 
            check=True,
        )


def on_close_window():
    root.quit()
    root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Lenia Visualization")
    controller = Controller(root)
    controller.import_lenia("DefaultLeniaConfig")
    root.protocol("WM_DELETE_WINDOW", on_close_window)
    root.mainloop()
