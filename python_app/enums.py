from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    VERIFYING = auto()
    OPENING = auto()
    OPEN = auto()
    CLOSING = auto()

class ServoNum(Enum):
    SERVO1 = auto()
    SERVO2 = auto()
    SERVO3 = auto()
    SERVO4 = auto()
