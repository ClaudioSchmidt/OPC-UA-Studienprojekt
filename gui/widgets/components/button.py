from gui.widgets.components.base import BaseComponent
from model.enum import LedStateEnum
from PySide6.QtGui import QPixmap, QPainter

class LampButtonComponent(BaseComponent):
    def __init__(self, grid_x, grid_y, logical_width, logical_height, image_paths, button_attr):
        super().__init__(grid_x, grid_y, logical_width, logical_height)
        
        self.images = {
            name: QPixmap(path) for name, path in image_paths.items()
        }

        self.button_attr = button_attr

        self.is_pressed = False
        self.pattern = LedStateEnum.OFF

        self.blink_state = False
        self.blink_counter = 0

    def update(self, state):
        pass

    def sync_with_machine(self, machine, get_attr):
        button = get_attr(machine, self.button_attr)
        if button:
            self.is_pressed = button.is_pressed
            self.pattern = button.led_pattern
        else:
            self.is_pressed = False
            self.pattern = LedStateEnum.OFF

    def animate(self):
        if self.pattern == LedStateEnum.BLINKING:
            toggle_frames = 10    # 0.5 sec at 20 FPS
        elif self.pattern == LedStateEnum.SLOWBLINKING:
            toggle_frames = 20    # 1 sec at 20 FPS
        else:
            toggle_frames = 0

        if toggle_frames > 0:
            self.blink_counter += 1
            if self.blink_counter >= toggle_frames:
                self.blink_counter = 0
                self.blink_state = not self.blink_state
        else:
            self.blink_state = False
            self.blink_counter = 0

    def draw(self, painter: QPainter, cell_size: float):
        if self.pattern == LedStateEnum.OFF or (self.blink_state is False and self.pattern != LedStateEnum.ON):
            key = "off_pressed" if self.is_pressed else "off"
        else:
            key = "on_pressed" if self.is_pressed else "on"

        pixmap = self.images.get(key)
        if not pixmap or pixmap.isNull():
            return

        width = self.logical_width * cell_size
        height = self.logical_height * cell_size
        x = self.grid_x * cell_size
        y = self.grid_y * cell_size

        painter.save()
        painter.translate(x, y)
        painter.drawPixmap(0, 0, int(width), int(height), pixmap)
        painter.restore()
