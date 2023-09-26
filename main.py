import os
import tkinter as tk
from tkinter import filedialog, messagebox
import imageio.v2 as imageio  # Explicitly use v2 as recommended
from PIL import Image
import numpy as np

class MovieMaker:
    def __init__(self, folder_path, save_path, frame_duration):
        self.folder_path = folder_path
        self.save_path = save_path
        self.fps = 1.0 / frame_duration

    def create_movie(self):
        files = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f)) and f.endswith(".png")]
        files.sort(key=lambda x: int(x.split('_')[0]))

        with imageio.get_writer(self.save_path, mode='I', fps=self.fps) as writer:
            for filename in files:
                image_path = os.path.join(self.folder_path, filename)
                
                # Use PIL to open and convert the image to RGB
                pil_image = Image.open(image_path).convert("RGB")
                
                # Convert the PIL image back to a numpy array for imageio
                image_array = np.array(pil_image)
                
                writer.append_data(image_array)

class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Maker")

        self.label = tk.Label(root, text="Enter frame duration (seconds):")
        self.label.pack(pady=20)

        vcmd = (self.root.register(self.validate_entry), '%P')  # validation command
        self.entry = tk.Entry(root, validate="key", validatecommand=vcmd)
        self.entry.pack(pady=20)
        self.entry.insert(0, "1.0")  # default value

        # Label to display the FPS
        self.fps_label = tk.Label(root, text=self.calculate_fps_text())
        self.fps_label.pack(pady=10)

        self.entry.bind('<KeyRelease>', self.on_entry_update)

        self.button = tk.Button(root, text="Create Movie", command=self.create_movie)
        self.button.pack(pady=20)

        self.root.mainloop()

    def validate_entry(self, value):
        # Check if the entry is empty or a valid positive float
        if value == "":
            return True
        try:
            float_val = float(value)
            return float_val > 0
        except ValueError:
            return False

    def calculate_fps_text(self):
        # Calculate FPS from the entry value and return the display text
        try:
            fps = 1.0 / float(self.entry.get())
            return f"FPS: {fps:.2f}"
        except (ValueError, ZeroDivisionError):
            return "Invalid value"

    def on_entry_update(self, event=None):
        # Update the FPS label when the entry changes
        self.fps_label.config(text=self.calculate_fps_text())

    def create_movie(self):
        frame_duration = float(self.entry.get())

        self.folder_path = self.get_folder_path()
        if not self.folder_path:
            return

        self.save_path = self.get_save_path()
        if not self.save_path:
            return

        self.movie_maker = MovieMaker(self.folder_path, self.save_path, frame_duration)
        self.movie_maker.create_movie()

        messagebox.showinfo("Success", f"Movie saved at {self.save_path}")

    def get_folder_path(self):
        return filedialog.askdirectory()

    def get_save_path(self):
        return filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
