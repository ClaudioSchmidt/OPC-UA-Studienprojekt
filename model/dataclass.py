from dataclasses import dataclass, field
from typing import List, Optional
from .enum import (SurfaceEnum, LedStateEnum, StatusCodeEnum, LabProgressEnum,
                    MainStateEnum, SubStateEnum, decode_machine_state)

@dataclass
class ButtonState:
    is_pressed: bool
    led_pattern: LedStateEnum

@dataclass
class SlideBuffer:
    count: int
    contents: List[SurfaceEnum] = field(default_factory=list)

@dataclass
class LabGroup:
    group_letter: str
    member_names: List[str]
    lab_progress: LabProgressEnum

@dataclass
class LabGroupSession:
    """
    Represents lab group assignment for session persistence.
    """
    uuid: str
    machine_id: int
    group_letter: str
    member_names: List[str]
    lab_part: int

@dataclass
class Machine:
    machine_id: int
    sorting_state: int
    remote_control_is_enabled: bool
    status_code: StatusCodeEnum
    sorting_criterion: SurfaceEnum
    workpiece_slide_a: SlideBuffer
    workpiece_slide_b: SlideBuffer
    app_button: ButtonState
    process_button: ButtonState
    fault_ack_button: ButtonState
    emergency_button: ButtonState
    belt_speed: float
    belt_speed_level: int
    is_running: bool
    is_reverse: bool
    switch: bool
    start_sensor: bool
    id_sensor: bool
    color_channel: int
    inductive_sensor: bool
    switch_sensor: bool
    storage_sensor: bool
    assigned_lab_group: Optional[LabGroup] = None

    def get_machine_states(self) -> tuple[MainStateEnum, SubStateEnum]:
        return decode_machine_state(self.sorting_state)