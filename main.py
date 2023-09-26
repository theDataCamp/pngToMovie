import os
import tkinter as tk
from tkinter import filedialog, messagebox
import imageio


class MovieMaker:
    def __init__(self, folder_path, save_path):
        self.folder_path = folder_path
        self.save_path = save_path

    def create_movie(self):
        files = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f)) and f.endswith(".png")]
        files.sort(key=lambda x: int(x.split('_')[0]))

        with imageio.get_writer(self.save_path, mode='I') as writer:
            for filename in files:
                image = imageio.imread(os.path.join(self.folder_path, filename))
                writer.append_data(image)


class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()

        self.folder_path = self.get_folder_path()
        if not self.folder_path:
            return

        self.save_path = self.get_save_path()
        if not self.save_path:
            return

        self.movie_maker = MovieMaker(self.folder_path, self.save_path)
        self.movie_maker.create_movie()

        messagebox.showinfo("Success", f"Movie saved at {self.save_path}")

    def get_folder_path(self):
        return filedialog.askdirectory()

    def get_save_path(self):
        return filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])


if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
