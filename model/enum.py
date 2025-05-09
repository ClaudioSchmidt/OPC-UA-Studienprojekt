from enum import Enum

class SurfaceEnum(Enum):
    UNDEFINED = 0
    BLACKSURFACE = 1
    REDSURFACE = 2
    METALLICSURFACE = 3

class LedStateEnum(Enum):
    OFF = 0
    ON = 1
    BLINKING = 2
    SLOWBLINKING = 3

class LabProgressEnum(Enum):
    PART1 = 0
    PART2 = 1
    PART3 = 2
    PART4 = 3
    FINISHED = 4

class SortingStateEnum(Enum):
    IDLE = 0
    ACTIVE = 1
    TEACHING = 2

class StatusCodeEnum(Enum):
    OK = 0
    ERROR = 1
    WARNING = 2
