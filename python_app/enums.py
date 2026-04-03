from enum import Enum, auto

class State(Enum):
    IDLE = auto()
    OPENING = auto()
    OPEN = auto()
    CLOSING = auto()

