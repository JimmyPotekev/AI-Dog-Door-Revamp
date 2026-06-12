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
    # MESSAGES TO CAMERA PROCESS(camera_proc_main)
    CAMERA_ON = auto()      # wakes the camera process
    CAMERA_OFF = auto()     # puts the camera process to sleep until woken
    SLEEP_TIMEOUT = auto()  # signals the camera process to sleep, pausing object detection until timeout
    SHUTDOWN = auto()       # stops the camera process
    # MESSAGES FROM CAMERA PROCESS
    DOG_FOUND = auto()      # signals ot the main process that a dog was found in the image
    NO_DOG_FOUND = auto()   # signals to the main process that a dog was not found in the image
