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

class CameraComm(Enum):
    CAPTURE_IMG = auto()
    POWERUP = auto()        # 
    SHUTDOWN = auto()       #
    DOG_FOUND = auto()      # 
    NO_DOG_FOUND = auto()   # signals to the main process that a dog was not found in the image
    SLEEP_TIMEOUT = auto()  # signals the camera process to sleep, pausing object detection until timeout