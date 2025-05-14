from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt

class DeviceGrid(QWidget):
    def __init__(self, aspect_ratio=3/2):
        super().__init__()
        self.aspect_ratio = aspect_ratio
        self.panels = []

        self.grid = QGridLayout(self)
        self.grid.setSpacing(20)
        self.grid.setAlignment(Qt.AlignCenter)

    def set_panels(self, panels):
        # Clear grid
        while self.grid.count():
            child = self.grid.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

        self.panels = panels
        if not panels:
            label = QLabel("No Devices connected")
            label.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(label, 0, 0)
            return

        # Add widgets in grid
        columns = min(3, len(panels))
        for i, panel in enumerate(panels):
            row, col = divmod(i, columns)
            self.grid.addWidget(panel, row, col)

        self._resize_panels()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._resize_panels()

    def _resize_panels(self):
        n = len(self.panels)
        if n == 0:
            return

        columns = min(3, n)
        rows = (n + columns - 1) // columns
        spacing = self.grid.spacing()

        available_width = self.width() - spacing * (columns + 1)
        available_height = self.height() - spacing * (rows + 1)

        max_width = available_width / columns
        max_height = available_height / rows

        # Aspect ratio math
        width_based_height = max_width / self.aspect_ratio
        height_based_width = max_height * self.aspect_ratio

        if width_based_height <= max_height:
            panel_w, panel_h = max_width, width_based_height
        else:
            panel_w, panel_h = height_based_width, max_height

        for panel in self.panels:
            panel.setFixedSize(round(panel_w), round(panel_h))
