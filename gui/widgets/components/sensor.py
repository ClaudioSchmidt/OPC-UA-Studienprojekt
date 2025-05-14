from gui.widgets.components.base import BaseComponent
from PySide6.QtGui import QPixmap, QPainter
import math

PULSE_SPEED = 0.85
PULSE_AMPLITUDE = 0.1

class BaseSensorComponent(BaseComponent):
    def __init__(self, grid_x, grid_y, logical_width, logical_height,
                image_path, rotation_angle=0, sensor_name=None, pulse_origin_offset=(0.5, 0.5)):
        super().__init__(grid_x, grid_y, logical_width, logical_height, rotation_angle)
        self.image = QPixmap(image_path)
        self.sensor_name = sensor_name
        self.is_active = False
        self.pulse_state = 0.0
        self.pulse_origin_offset = pulse_origin_offset

    def update(self, state):
        self.is_active = state

    def sync_with_machine(self, machine, get_attr):
        if self.sensor_name:
            value = get_attr(machine, self.sensor_name)
            self.is_active = bool(value)

    def animate(self):
        if self.is_active:
            self.pulse_state += PULSE_SPEED
        else:
            self.pulse_state = 0.0

    def should_draw(self):
        return True

    def draw(self, painter: QPainter, cell_size: float):
        if not self.should_draw() or self.image.isNull():
            return

        width = self.logical_width * cell_size
        height = self.logical_height * cell_size
        x = self.grid_x * cell_size
        y = self.grid_y * cell_size

        painter.save()

        # Step 1: anchor to grid_x, grid_y for rotation
        painter.translate(x, y)
        painter.rotate(self.rotation_angle)

        # Step 2: manual pulse origin
        origin_x = width * self.pulse_origin_offset[0]
        origin_y = height * self.pulse_origin_offset[1]
        painter.translate(origin_x, origin_y)

        # Step 3: scale
        scale = 1.0
        if self.is_active:
            scale = 1.0 + PULSE_AMPLITUDE * math.sin(self.pulse_state)
        painter.scale(scale, scale)

        # Step 4: move back
        painter.translate(-origin_x, -origin_y)

        # Step 5: draw image
        painter.drawPixmap(0, 0, int(width), int(height), self.image)

        painter.restore()



class SensorComponent(BaseSensorComponent):
    def should_draw(self):
        return True


class SensorHighlightComponent(BaseSensorComponent):
    def should_draw(self):
        return self.is_active
