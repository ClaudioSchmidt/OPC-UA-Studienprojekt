from abc import ABC, abstractmethod
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import QRectF

class BaseComponent(ABC):
    def __init__(self, grid_x, grid_y, logical_width=1, logical_height=1, rotation_angle=0):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.logical_width = logical_width
        self.logical_height = logical_height
        self.rotation_angle = rotation_angle

        self.image = None

    @abstractmethod
    def update(self, state):
        pass

    @abstractmethod
    def sync_with_machine(self, machine, get_attr):
        pass

    @abstractmethod
    def draw(self, painter: QPainter, cell_size: float):
        pass

    def get_draw_rect(self, cell_size: float) -> QRectF:
        x = self.grid_x * cell_size
        y = self.grid_y * cell_size
        width = self.logical_width * cell_size
        height = self.logical_height * cell_size
        return QRectF(x, y, width, height)
    
    def animate(self):
       pass
