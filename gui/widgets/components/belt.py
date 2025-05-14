from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt
from gui.widgets.components.base import BaseComponent

class CachedBeltComponent(BaseComponent):
    def __init__(self, grid_x, grid_y, logical_width, logical_height, image_path):
        super().__init__(grid_x, grid_y, logical_width, logical_height)
        
        self.image = QPixmap(image_path)
        self.move_offset = 0.0
        self.move_speed = 0.15
        self.is_running = False
        self.is_reverse = False
        self.cache_image = None
        self.last_offset = None

    def update(self, state):
        pass

    def sync_with_machine(self, machine, get_attr):
        self.is_running = get_attr(machine, "is_running")
        self.is_reverse = get_attr(machine, "is_reverse")

    def animate(self):
        if self.is_running:
            if self.is_reverse:
                self.move_offset -= self.move_speed
            else:
                self.move_offset += self.move_speed
            
            self.move_offset = self.move_offset % 1.0

    def draw(self, painter: QPainter, cell_size: float):
        if self.image.isNull():
            return

        belt_width = int(self.logical_width * cell_size)  # Belt width
        belt_height = int(self.logical_height * cell_size)  # Belt height
        belt_x = int(self.grid_x * cell_size)  # Belt x position
        belt_y = int(self.grid_y * cell_size)  # Belt y position
        tile_width = int(cell_size)  # Width of one tile
        tile_height = int(2 * cell_size)  # Height of one tile

        scaled_tile = self.image.scaled(
            tile_width,
            tile_height,
        )

        pixel_offset = int(self.move_offset * tile_width)

        if self.cache_image is None or self.last_offset != pixel_offset:
            cache_width = belt_width + 2 * tile_width
            cache_height = belt_height
            self.cache_image = QPixmap(cache_width, cache_height)
            self.cache_image.fill(Qt.transparent)  # Clear cache

            cache_painter = QPainter(self.cache_image)
            x_position = -tile_width - (pixel_offset % tile_width)

            while x_position < cache_width:
                cache_painter.drawPixmap(int(x_position), 0, scaled_tile)
                x_position += tile_width

            cache_painter.end()
            self.last_offset = pixel_offset

        painter.save()
        painter.translate(belt_x, belt_y)
        painter.setClipRect(0, 0, belt_width, belt_height)
        painter.drawPixmap(0, 0, self.cache_image, tile_width, 0, belt_width, belt_height)
        painter.restore()