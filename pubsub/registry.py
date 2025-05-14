from model import Machine, SlideBuffer, ButtonState
from model import LedStateEnum
from typing import Dict, Optional, Any, Callable, List

class MachineRegistry:
    def __init__(self):
        # Dictionary to hold machine instances, keyed by machine_id
        self._machines: Dict[int, Machine] = {}
        # List to hold callback functions for machines
        self._callbacks: List[Callable[[Machine, bool], None]] = []  

    def register_callback(self, callback: Callable[[Machine], None]):
        self._callbacks.append(callback)

    def _add_machine(self, machine_id: int, data: Dict[str, Any]) -> Machine:
        """
        Creates a new Machine instance, assuming the publisher sends all required fields.
        """
        return Machine(
            machine_id=machine_id,
            sorting_state=data["sorting_state"],
            remote_control_is_enabled=data["remote_control_is_enabled"],
            status_code=data["status_code"],
            sorting_criterion=data["sorting_criterion"],
            workpiece_slide_a=SlideBuffer(
                count=data.get("workpiece_counter_slide_a", 0),
                contents=[]
            ),
            workpiece_slide_b=SlideBuffer(
                count=data.get("workpiece_counter_slide_b", 0),
                contents=[]
            ),
            app_button=ButtonState(
                is_pressed=data["app_btn"],
                led_pattern=LedStateEnum(data["app_led"])
            ),
            process_button=ButtonState(
                is_pressed=data["process_btn"],
                led_pattern=LedStateEnum(data["process_led"])
            ),
            fault_ack_button=ButtonState(
                is_pressed=data["fault_ack_btn"],
                led_pattern=LedStateEnum(data["fault_ack_led"])
            ),
            emergency_button=ButtonState(
                is_pressed=data["emergency_btn"],
                led_pattern=LedStateEnum(0)
            ),
            belt_speed=data["belt_speed"],
            belt_speed_level=data["belt_speed_level"],
            is_running=data["is_running"],
            is_reverse=data["is_reverse"],
            switch=data["switch"],
            start_sensor=data["start_sensor"],
            id_sensor=data["id_sensor"],
            color_channel=data["color_channel"],
            inductive_sensor=data["inductive_sensor"],
            switch_sensor=data["switch_sensor"],
            storage_sensor=data["storage_sensor"],
            assigned_lab_group=None
        )
    
    def update_machine(self, machine_id: int, data: Dict[str, Any]) -> None:
        if machine_id not in self._machines:
            machine = self._add_machine(machine_id, data)
            self._machines[machine_id] = machine
            for callback in self._callbacks:
                callback(machine, True)  # notify new machine
                #print(f"[Registry] New machine added: {machine_id}")
        else:
            machine = self._machines[machine_id]
            for key, value in data.items():
                setattr(machine, key, value)
            for callback in self._callbacks:
                callback(machine, False)  # notify updated machine
                #print(f"[Registry] Machine updated: {machine_id}")

    def get_machine(self, machine_id: int) -> Optional[Machine]:
        return self._machines.get(machine_id)

    def get_all_machines(self) -> list[Machine]:
        return list(self._machines.values())