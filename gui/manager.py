import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QHBoxLayout, QScrollArea, QGridLayout
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QObject, Signal

from gui.widgets.widget_machine import MachineWidget
from gui.widgets.widget_device_grid import DeviceGrid
from gui.utils.machine_animator import MachineAnimator

# ------------------------------
# THREADING ERROR EXPLANATION:
#
# Problem:
# Subscriber runs in worker thread and called GUI update directly -> Qt disallowed this
# ("QObject::setParent: Cannot set parent, new parent is in a different thread")
#
# Why:
# Qt requires all widgets to be created/modified ONLY in the main GUI thread
#
# Solution:
# Use Signal -> emit() from worker thread → Qt safely delivers to slot in GUI thread
# ------------------------------


class GUIManager(QObject):
    machine_update_signal = Signal(object, bool)

    def __init__(self, flask_ip: str, registry):
        super().__init__()

        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.flask_ip = flask_ip
        self.registry = registry

        self.machine_widgets = {}

        self.setup_window()
        self.setup_layout()

        self.animator = MachineAnimator(self, fps=20)
        self.animator.start()

        # Connect signal to slot
        self.machine_update_signal.connect(self._handle_machine_update)

        # Register callback in MachineRegistry
        # SubscriberClient calls this
        self.registry.register_callback(self._registry_callback)

    def setup_window(self):
        self.window.setWindowTitle("OPC UA LAB UI")
        self.window.resize(1280, 720)

    def setup_layout(self):
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        layout.addWidget(self.create_header())
        layout.addWidget(self.create_body(), stretch=1)
        layout.addWidget(self.create_footer())

        self.window.setCentralWidget(central_widget)

    def create_header(self):
        header = QWidget()
        layout = QHBoxLayout(header)

        left_logo = QLabel()
        left_logo.setPixmap(QPixmap("gui/assets/opcua_logo.png").scaledToHeight(48, Qt.SmoothTransformation))
        left_logo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(left_logo)

        layout.addStretch(1)

        right_logo = QLabel()
        right_logo.setPixmap(QPixmap("gui/assets/esslingen_university_logo.png").scaledToHeight(68, Qt.SmoothTransformation))
        right_logo.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(right_logo)

        return header

    def create_body(self):
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        container = QWidget()
        layout = QVBoxLayout(container)

        self.device_grid = DeviceGrid(aspect_ratio=3/2)
        layout.addWidget(self.device_grid)

        container.setLayout(layout)
        self.scroll_area.setWidget(container)
        return self.scroll_area

    def create_footer(self):
        footer = QWidget()
        layout = QHBoxLayout(footer)

        info_label = QLabel(f"<b>Assign machines here:</b><br>{self.flask_ip}")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("font-size: 18px;")
        layout.addWidget(info_label)

        return footer
    
    def rebuild_grid(self):
        row_size = 3
        widgets = list(self.machine_widgets.values())

        for i in reversed(range(self.machine_layout.count())):
            item = self.machine_layout.itemAt(i)
            if item.widget():
                item.widget().setParent(None)

        for index, widget in enumerate(widgets):
            row = index // row_size
            col = index % row_size
            self.machine_layout.addWidget(widget, row, col)

    # Callback function for MachineRegistry
    # This is called from the worker thread
    # and emits a signal to update the GUI
    def _registry_callback(self, machine, is_new):
        self.machine_update_signal.emit(machine, is_new)

    def _handle_machine_update(self, machine, is_new: bool):
        machine_id = machine.machine_id

        if is_new:
            widget = MachineWidget(machine, aspect_ratio=3/2)
            self.machine_widgets[machine_id] = widget
        else:
            widget = self.machine_widgets.get(machine_id)
            if widget:
                widget.update_components(machine)

        all_panels = list(self.machine_widgets.values())
        self.device_grid.set_panels(all_panels)

    def show(self):
        self.window.show()
        sys.exit(self.app.exec())
