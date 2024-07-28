import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QColorDialog, QGridLayout, QLabel
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QTimer
import random
import colorsys

class ColorGenerator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Absurd Color Generator")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.color_label = QLabel("Generated Colors:")
        self.color_label.setStyleSheet("font-size: 24px;")
        self.layout.addWidget(self.color_label)

        self.color_grid = QGridLayout()
        self.layout.addLayout(self.color_grid)

        self.generate_button = QPushButton("Generate New Colors")
        self.generate_button.clicked.connect(self.generate_colors)
        self.layout.addWidget(self.generate_button)

        self.pick_color_button = QPushButton("Pick Color")
        self.pick_color_button.clicked.connect(self.pick_color)
        self.layout.addWidget(self.pick_color_button)

        self.save_palette_button = QPushButton("Save Palette")
        self.save_palette_button.clicked.connect(self.save_palette)
        self.layout.addWidget(self.save_palette_button)

        self.load_palette_button = QPushButton("Load Palette")
        self.load_palette_button.clicked.connect(self.load_palette)
        self.layout.addWidget(self.load_palette_button)

        self.color_displays = []

        self.generate_colors()

    def generate_colors(self):
        for display in self.color_displays:
            display.deleteLater()
        self.color_displays = []

        for i in range(5):
            colors = []
            for _ in range(3):
                hue = random.random()
                saturation = random.random()
                value = random.random()
                color = colorsys.hsv_to_rgb(hue, saturation, value)
                color = tuple(int(channel * 255) for channel in color)
                colors.append(color)

            display = QWidget()
            display_layout = QGridLayout()
            display.setLayout(display_layout)

            for j, color in enumerate(colors):
                label = ColorLabel(color)
                label.setFixedSize(100, 100)
                display_layout.addWidget(label, 0, j)

            self.color_grid.addWidget(display, i, 0)
            self.color_displays.append(display)

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            label = ColorLabel(color)
            label.setFixedSize(100, 100)
            self.color_grid.addWidget(label, len(self.color_displays), 0)
            self.color_displays.append(label)

    def save_palette(self):
        with open("palette.txt", "w") as f:
            for display in self.color_displays:
                for label in display.findChildren(ColorLabel):
                    color = label.color
                    f.write(f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}\n")

    def load_palette(self):
        try:
            with open("palette.txt", "r") as f:
                colors = [line.strip() for line in f.readlines()]
                for i, color in enumerate(colors):
                    label = ColorLabel(QColor(color))
                    label.setFixedSize(100, 100)
                    self.color_grid.addWidget(label, i // 3, i % 3)
                    self.color_displays.append(label)
        except FileNotFoundError:
            print("Palette file not found.")

class ColorLabel(QLabel):
    def __init__(self, color):
        super().__init__()

        self.color = color
        if isinstance(color, QColor):
            self.color = (color.red(), color.green(), color.blue())

        self.setStyleSheet(f"background-color: #{self.color[0]:02x}{self.color[1]:02x}{self.color[2]:02x}; border: 1px solid black;")

        self.hovered = False
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate)
        self.animation_frame = 0

    def enterEvent(self, event):
        self.hovered = True
        self.animation_timer.start(50)

    def leaveEvent(self, event):
        self.hovered = False
        self.animation_timer.stop()
        self.animation_frame = 0
        self.setStyleSheet(f"background-color: #{self.color[0]:02x}{self.color[1]:02x}{self.color[2]:02x}; border: 1px solid black;")

    def animate(self):
        if self.hovered:
            self.animation_frame += 1
            if self.animation_frame % 2 == 0:
                self.setStyleSheet(f"background-color: #{self.color[0]:02x}{self.color[1]:02x}{self.color[2]:02x}; border: 1px solid red;")
            else:
                self.setStyleSheet(f"background-color: #{self.color[0]:02x}{self.color[1]:02x}{self.color[2]:02x}; border: 1px solid black;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorGenerator()
    window.show()
    sys.exit(app.exec_())
