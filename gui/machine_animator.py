from PySide6.QtCore import QTimer

class MachineAnimator:
    def __init__(self, gui_manager, fps=20):
        self.gui_manager = gui_manager
        self.interval = int(1000 / fps)
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)

    def start(self):
        self.timer.start(self.interval)

    def stop(self):
        self.timer.stop()

    def tick(self):
        for widget in self.gui_manager.machine_widgets.values():
            for component in widget.components:
                if hasattr(component, "animate"):
                    component.animate()
            widget.visualization.update()
