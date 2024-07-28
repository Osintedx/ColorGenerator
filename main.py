import tkinter as tk
from tkinter import ttk
import colorsys
import random

class ColorGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Absurd Color Generator")

        self.color_label = tk.Label(root, text="Generated Colors:", font=("Arial", 16))
        self.color_label.pack(pady=10)

        self.color_frame = tk.Frame(root)
        self.color_frame.pack()

        self.generate_button = tk.Button(root, text="Generate New Colors", command=self.generate_colors)
        self.generate_button.pack(pady=10)

        self.color_displays = []

        self.generate_colors()

    def generate_colors(self):
        for display in self.color_displays:
            display.destroy()
        self.color_displays = []

        for _ in range(5):
            colors = []
            for _ in range(3):
                hue = random.random()
                saturation = random.random()
                value = random.random()
                color = colorsys.hsv_to_rgb(hue, saturation, value)
                color = tuple(int(channel * 255) for channel in color)
                colors.append(color)

            display = tk.Frame(self.color_frame)
            display.pack(pady=10)

            for i, color in enumerate(colors):
                label = tk.Label(display, bg="#{:02x}{:02x}{:02x}".format(*color), width=10, height=5)
                label.pack(side=tk.LEFT, padx=5)

            self.color_displays.append(display)

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorGenerator(root)
    root.mainloop()
