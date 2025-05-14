from PySide6.QtGui import QPainter, QPixmap
from gui.widgets.components.base import BaseComponent

class StaticBackgroundComponent(BaseComponent):
    def __init__(self, grid_x, grid_y, logical_width, logical_height, image_path):
        super().__init__(grid_x, grid_y, logical_width, logical_height)
        self.image = QPixmap(image_path)

    def update(self, state):
        pass

    def sync_with_machine(self, machine, get_attr):
        pass

    def draw(self, painter: QPainter, cell_size: float):
        rect = self.get_draw_rect(cell_size)
        if not self.image.isNull():
            painter.drawPixmap(rect, self.image, self.image.rect())