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

class MainStateEnum(IntEnum):
    APP_START = 0
    APP_FAULT = 1
    EMERGENCY_STOP = 2
    REMOTE_CONTROL = 3
    PROCESS_DISABLED = 4
    PROCESS_ENABLED = 5

class SubStateEnum(IntEnum):
    NONE_SUB_STATE = 0

    # ProcessDisabled substates
    IDLE = 1
    INITIALIZING = 2
    ACTIVE = 3
    TEACHING_ENABLED = 4
    TEACHING_WAITING_FOR_ID_SENSOR = 5
    TEACHING_PROGRAM_COLOR_SENSOR = 6
    TEACHING_WAITING_FOR_STORAGE_SENSOR = 7

    # ProcessEnabled substates
    WAITING = 8
    SORTING_WAITING_FOR_ID_SENSOR = 9
    SORTING_IDENTIFICATION = 10
    SORTING_WAITING_FOR_STORAGE_SENSOR = 11
    SORTING_WAITING_FOR_SWITCH_SENSOR = 12
    HALTED = 13
    PROCESS_FAULT = 14
    STORAGE_FULL = 15

def encode_machine_state(main_state: MainStateEnum, sub_state: SubStateEnum) -> int:
    # <<: shifts bits to the left by 4 positions
    # |: bitwise OR operation
    return (main_state << 4) | sub_state

def decode_machine_state(byte_value: int) -> tuple[MainStateEnum, SubStateEnum]:
    main_state_value = byte_value >> 4 # Shift right by 4 to get the main state
    sub_state_value = byte_value & 0x0F  # Mask to get the last 4 bits
    return MainStateEnum(main_state_value), SubStateEnum(sub_state_value)
