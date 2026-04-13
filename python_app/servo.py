# General
from abc import ABC, abstractmethod
# Enums
from .enums import ServoNum

# logger
from logging import getLogger

logger = getLogger(__name__)

class ServoIntf(ABC):

    @abstractmethod
    def open(self) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass
    

class RealServo(ServoIntf):

    def __init__(self, servo_num: ServoNum) -> None:
        logger.info("Initializing Servo")
        self.servo_num: ServoNum = servo_num
        logger.info("Servo setup complete")


    def open(self) -> None:
        pass


    def close(self) -> None:
        pass
    

class FakeServo(ServoIntf):

    def __init__(self, servo_num: ServoNum) -> None:
        logger.info("Initializing FakeServo")
        self.servo_num: ServoNum = servo_num
        logger.info("FakeServo setup complete")


    def open(self) -> None:
        logger.info("Servo %s setting to 90 degrees", self.servo_num)


    def close(self) -> None:
        logger.info("Servo %s setting to 0 degrees", self.servo_num)
    