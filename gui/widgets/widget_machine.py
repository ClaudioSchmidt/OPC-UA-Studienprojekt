from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor, QPen

from gui.widgets.components.static_background import StaticBackgroundComponent
from gui.widgets.components.sensor import SensorComponent, SensorHighlightComponent
from gui.widgets.components.belt import CachedBeltComponent
from gui.widgets.components.switch import ArmComponent
from gui.widgets.components.button import LampButtonComponent

class MachineVisualizationCanvas(QWidget):
    def __init__(self, grid_width, grid_height, parent=None):
        super().__init__(parent)
        self.grid_size = (grid_width, grid_height)
        self.components = []
        self.setStyleSheet("background-color: white; border: 1px solid black;")

    def set_grid_size(self, width, height):
        self.grid_size = (width, height)
        self.update()

    def set_components(self, components):
        self.components = components
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        
        painter.setRenderHint(QPainter.SmoothPixmapTransform, False)
        painter.setRenderHint(QPainter.Antialiasing, False)

        widget_width = self.width()
        widget_height = self.height()
        grid_cols, grid_rows = self.grid_size

        # calculate grid cell size
        cell_size_x = widget_width / grid_cols
        cell_size_y = widget_height / grid_rows
        cell_size = min(cell_size_x, cell_size_y)  # force 1:1

        # center grid
        total_grid_width = cell_size * grid_cols
        total_grid_height = cell_size * grid_rows
        offset_x = (widget_width - total_grid_width) / 2
        offset_y = (widget_height - total_grid_height) / 2

        painter.translate(offset_x, offset_y)

        # draw components (background first!)
        for component in self.components:
            component.draw(painter, cell_size)

        # draw grid lines on top
        #pen = QPen(QColor(200, 200, 200), 1)
        #painter.setPen(pen)

        #for x in range(grid_cols + 1):
        #    x_pos = x * cell_size
        #    painter.drawLine(x_pos, 0, x_pos, total_grid_height)

        #for y in range(grid_rows + 1):
        #    y_pos = y * cell_size
        #    painter.drawLine(0, y_pos, total_grid_width, y_pos)

        painter.end()

    def sizeHint(self):
        return QSize(400, 320)

class MachineWidget(QWidget):
    def __init__(self, machine, aspect_ratio=3/2):
        super().__init__()
        self.machine = machine
        self.aspect_ratio = aspect_ratio
        self.components = []

        layout = QHBoxLayout(self)

        #Left Panel
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)

        name_label = QLabel(f"Machine ID: {machine.machine_id}")
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        left_layout.addWidget(name_label)

        # canvas grid size
        self.visualization = MachineVisualizationCanvas(grid_width=17, grid_height=16)
        left_layout.addWidget(self.visualization, stretch=1)

        layout.addWidget(left_panel, stretch=3)

        # Right Panel 
        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: #f0f0f0; border: 1px solid #aaa;")
        layout.addWidget(right_panel, stretch=1)

        # set components
        background = StaticBackgroundComponent(
            grid_x=0,
            grid_y=0,
            logical_width=17,
            logical_height=16,
            image_path="gui/assets/bottom.png"
        )
        self.components.append(background)

        belt = CachedBeltComponent(
            grid_x=1,
            grid_y=2,
            logical_width=15,
            logical_height=2,
            image_path="gui/assets/belt_segment.png"
        )
        self.components.append(belt)

        arm = ArmComponent(
            grid_x=3,
            grid_y=0.5,
            logical_width=4,
            logical_height=1,
            image_path="gui/assets/sorting_arm.png",
            pivot_offset=(0.875, 0.4),
            sensor_name="switch",
            open_angle=0,
            closed_angle=-45
        )
        self.components.append(arm)

        app_lamp = LampButtonComponent(
            grid_x=7.5,
            grid_y=13,
            logical_width=2,
            logical_height=2,
            image_paths={
                "off": "gui/assets/button_app_off.png",
                "off_pressed": "gui/assets/button_app_off_pressed.png",
                "on": "gui/assets/button_app_on.png",
                "on_pressed": "gui/assets/button_app_on_pressed.png"
            },
            button_attr="app_button"
        )
        self.components.append(app_lamp)

        process_lamp = LampButtonComponent(
            grid_x=10.5,
            grid_y=13,
            logical_width=2,
            logical_height=2,
            image_paths={
                "off": "gui/assets/button_process_off.png",
                "off_pressed": "gui/assets/button_process_off_pressed.png",
                "on": "gui/assets/button_process_on.png",
                "on_pressed": "gui/assets/button_process_on_pressed.png"
            },
            button_attr="process_button"
        )
        self.components.append(process_lamp)

        faultack_lamp = LampButtonComponent(
            grid_x=13.5,
            grid_y=13,
            logical_width=2,
            logical_height=2,
            image_paths={
                "off": "gui/assets/button_faultack_off.png",
                "off_pressed": "gui/assets/button_faultack_off_pressed.png",
                "on": "gui/assets/button_faultack_on.png",
                "on_pressed": "gui/assets/button_faultack_on_pressed.png"
            },
            button_attr="fault_ack_button"
        )
        self.components.append(faultack_lamp)

        start_sensor = SensorComponent(
            grid_x=14,
            grid_y=4,
            logical_width=1,
            logical_height=1,
            image_path="gui/assets/optical_sensor.png",
            rotation_angle=0,
            sensor_name="start_sensor",
            pulse_origin_offset=(0.5, 0)
        )
        self.components.append(start_sensor)

        start_sensor_highlight = SensorHighlightComponent(
            grid_x=14,
            grid_y=2,
            logical_width=1,
            logical_height=2,
            image_path="gui/assets/sensor_highlight.png",
            rotation_angle=0,
            sensor_name="start_sensor",
            pulse_origin_offset=(0.5, 1)
        )
        self.components.append(start_sensor_highlight)

        id_sensor = SensorComponent(
            grid_x=11,
            grid_y=4,
            logical_width=1,
            logical_height=1.5,
            image_path="gui/assets/id_sensor.png",
            rotation_angle=0,
            sensor_name="id_sensor",
            pulse_origin_offset=(0.5, 0)
        )
        self.components.append(id_sensor)

        id_sensor_highlight = SensorHighlightComponent(
            grid_x=11,
            grid_y=2,
            logical_width=1,
            logical_height=2,
            image_path="gui/assets/sensor_highlight.png",
            rotation_angle=0,
            sensor_name="id_sensor",
            pulse_origin_offset=(0.5, 1)
        )
        self.components.append(id_sensor_highlight)

        id_color_sensor = SensorComponent(
            grid_x=10,
            grid_y=4,
            logical_width=1,
            logical_height=2,
            image_path="gui/assets/id_color_sensor.png",
            rotation_angle=0,
            sensor_name="color_channel",
            pulse_origin_offset=(0.5, 0)
        )
        self.components.append(id_color_sensor)

        id_color_sensor_highlight = SensorHighlightComponent(
            grid_x=10,
            grid_y=2,
            logical_width=1,
            logical_height=2,
            image_path="gui/assets/sensor_highlight_white.png",
            rotation_angle=0,
            sensor_name="color_channel",
            pulse_origin_offset=(0.5, 1)
        )
        self.components.append(id_color_sensor_highlight)

        inductive_sensor = SensorComponent(
            grid_x=9,
            grid_y=0,
            logical_width=2,
            logical_height=2,
            image_path="gui/assets/id_inductive_sensor.png",
            rotation_angle=0,
            sensor_name="inductive_sensor",
            pulse_origin_offset=(0.5, 0.5)
        )
        self.components.append(inductive_sensor)

        inductive_sensor_active = SensorHighlightComponent(
            grid_x=9,
            grid_y=0,
            logical_width=2,
            logical_height=2,
            image_path="gui/assets/id_inductive_sensor_active.png",
            rotation_angle=0,
            sensor_name="inductive_sensor",
            pulse_origin_offset=(0.5, 0.5)
        )
        self.components.append(inductive_sensor_active)

        switch_sensor = SensorComponent(
            grid_x=2,
            grid_y=2,
            logical_width=1,
            logical_height=1,
            image_path="gui/assets/optical_sensor.png",
            rotation_angle=180,
            sensor_name="switch_sensor",
            pulse_origin_offset=(0.5, 0)
        )
        self.components.append(switch_sensor)

        switch_sensor_highlight = SensorHighlightComponent(
            grid_x=2,
            grid_y=4,
            logical_width=1,
            logical_height=2,
            image_path="gui/assets/sensor_highlight.png",
            rotation_angle=180,
            sensor_name="switch_sensor",
            pulse_origin_offset=(0.5, 1)
        )
        self.components.append(switch_sensor_highlight)

        storage_sensor = SensorComponent(
            grid_x=6,
            grid_y=7,
            logical_width=1,
            logical_height=1.5,
            image_path="gui/assets/id_sensor.png",
            rotation_angle=270,
            sensor_name="storage_sensor",
            pulse_origin_offset=(0.5, 0)
        )
        self.components.append(storage_sensor)

        storage_sensor_highlight = SensorHighlightComponent(
            grid_x=2,
            grid_y=7,
            logical_width=1,
            logical_height=4,
            image_path="gui/assets/sensor_highlight.png",
            rotation_angle=270,
            sensor_name="storage_sensor",
            pulse_origin_offset=(0.5, 1)
        )
        self.components.append(storage_sensor_highlight)

        self.visualization.set_components(self.components)

    def get_nested_attr(self, obj, attr_path):
        if isinstance(attr_path, (list, tuple)):
            for attr in attr_path:
                obj = getattr(obj, attr, None)
                if obj is None:
                    return None
            return obj
        else:
            return getattr(obj, attr_path, None)

    def update_components(self, machine):
        self.machine = machine

        for component in self.components:
            component.sync_with_machine(machine, self.get_nested_attr)

        self.visualization.update()
