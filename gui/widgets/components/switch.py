from gui.widgets.components.base import BaseComponent
from PySide6.QtGui import QPixmap, QPainter

class ArmComponent(BaseComponent):
    def __init__(self, grid_x, grid_y, logical_width, logical_height,
                 image_path, pivot_offset=(0.5, 0.5), sensor_name="switch",
                 open_angle=0, closed_angle=-90):
        super().__init__(grid_x, grid_y, logical_width, logical_height)

        self.image = QPixmap(image_path)
        self.pivot_offset = pivot_offset
        self.sensor_name = sensor_name

        self.current_angle = open_angle
        self.target_angle = open_angle
        self.open_angle = open_angle
        self.closed_angle = closed_angle
        self.rotation_speed = 2.5  # degrees per frame

    def update(self, state):
        pass

    def sync_with_machine(self, machine, get_attr):
        is_closed = get_attr(machine, self.sensor_name)
        self.target_angle = self.closed_angle if is_closed else self.open_angle

    def animate(self):
        # Calculate difference between current and target
        angle_difference = self.target_angle - self.current_angle

        # If the difference is large enough → move toward target
        if abs(angle_difference) > self.rotation_speed:
            # Move by fixed step in correct direction
            step = self.rotation_speed if angle_difference > 0 else -self.rotation_speed
            self.current_angle += step
        else:
            # Close enough → snap exactly to target
            self.current_angle = self.target_angle

    def draw(self, painter: QPainter, cell_size: float):
        if self.image.isNull():
            return

        width = self.logical_width * cell_size
        height = self.logical_height * cell_size
        x = self.grid_x * cell_size
        y = self.grid_y * cell_size

        pivot_x = width * self.pivot_offset[0]
        pivot_y = height * self.pivot_offset[1]

        painter.save()
        painter.translate(x + pivot_x, y + pivot_y)
        painter.rotate(self.current_angle)
        painter.translate(-pivot_x, -pivot_y)

        painter.drawPixmap(0, 0, int(width), int(height), self.image)
        painter.restore()
