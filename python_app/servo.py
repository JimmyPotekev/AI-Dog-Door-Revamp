# Enums
from .enums import ServoNum

# logger
from logging import getLogger

logger = getLogger(__name__)

class Servo:

    def __init__(self, servo_num: ServoNum) -> None:
        logger.info("Initializing Servo")
        self.servo_num: ServoNum = servo_num
        logger.info("Servo setup complete")


    def open(self) -> None:
        pass


    def close(self) -> None:
        pass
    