from enum import IntEnum

class SurfaceEnum(IntEnum):
    UNDEFINED = 0
    BLACKSURFACE = 1
    REDSURFACE = 2
    METALLICSURFACE = 3

class LedStateEnum(IntEnum):
    OFF = 0
    ON = 1
    BLINKING = 2
    SLOWBLINKING = 3

class LabProgressEnum(IntEnum):
    PART1 = 0
    PART2 = 1
    PART3 = 2
    PART4 = 3
    FINISHED = 4

class StatusCodeEnum(IntEnum):

    INITIALIZATION_WAITING = 100
    INITIALIZATION_FAULT = 101
    INITIALIZATION_OK = 102
    INITIALIZING = 103
    
    SORTING = 104
    SORTING_HALTED = 105
    SORTING_UNEXPECTED = 106
    SORTING_READY = 107
    SORTING_TIMEOUT = 108
    
    EMERGENCY_PRESSED = 115
    EMERGENCY_RELEASED = 116
    STORAGE_FULL = 117
    TEACHING = 118
    
    REMOTECONTROL_READY = 120
    SPEED_DATACHANGE = 121
    DIRECTION_DATACHANGE = 122
    CRITERION_DATACHANGE = 123
    START_BELT_CALL = 124
    STOP_BELT_CALL = 125
    SWITCH_OPEN_CALL = 126
    SWITCH_CLOSE_CALL = 127
    REMOTECONTROL_ERROR = 128
    
    WORKPIECECOUNTER_RESET = 129
    
    STARTUP = 200
    OK = 201
    ERROR = 202

class MainState(IntEnum):
    AppStart = 0
    AppFault = 1
    EmergencyStop = 2
    RemoteControl = 3
    ProcessDisabled = 4
    ProcessEnabled = 5
    AppClosed = 6

class SubState(IntEnum):
    NoneState = 0

    # ProcessDisabled substates
    Idle = 1
    Initializing = 2
    Active = 3
    TeachingEnabled = 4
    TeachingWaitingForIdSensor = 5
    TeachingProgramColorSensor = 6
    TeachingWaitingForStorageSensor = 7

    # ProcessEnabled substates
    Waiting = 8
    SortingWaitingForIdSensor = 9
    SortingIdentification = 10
    SortingWaitingForStorageSensor = 11
    SortingWaitingForSwitchSensor = 12
    Halted = 13
    ProcessFault = 14
    StorageFull = 15

def encode_machine_state(main_state: MainState, sub_state: SubState) -> int:
    # <<: shifts bits to the left by 4 positions
    # |: bitwise OR operation
    return (main_state.value << 4) | sub_state.value

def decode_machine_state(byte_value: int) -> tuple[MainState, SubState]:
    main_state_value = byte_value >> 4 # Shift right by 4 to get the main state
    sub_state_value = byte_value & 0x0F  # Mask to get the last 4 bits
    return MainState(main_state_value), SubState(sub_state_value)
