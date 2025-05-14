from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class MachineWidget(QWidget):
    def __init__(self, machine):
        super().__init__()
        self.machine = machine

        layout = QVBoxLayout()
        label = QLabel(f"Machine ID: {machine.machine_id}")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.setLayout(layout)

    def update_components(self, machine):
        pass
