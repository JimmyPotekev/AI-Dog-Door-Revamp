from abc import ABC, abstractmethod
from adafruit_servokit import ServoKit
from .enums import ServoNum
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
    """
    Controls a single channel on a ServoKit board.
    Use RealServo.make_servos() to construct all four at once.
    """

    def __init__(self, kit: ServoKit, channel: int, servo_num: ServoNum) -> None:
        logger.info("Initializing RealServo %s on channel %d", servo_num.name, channel)
        self._servo = kit.servo[channel]
        self.servo_num = servo_num
        logger.info("RealServo %s setup complete", servo_num.name)

    @classmethod
    def make_servos(cls, channels: int = 16) -> list["RealServo"]:
        """
        Initializes the ServoKit and returns one RealServo per ServoNum,
        in ServoNum enum order. Call this instead of constructing RealServos manually.
        """
        kit = ServoKit(channels=channels)
        return [
            cls(kit, servo_num.value, servo_num)
            for servo_num in ServoNum
        ]

    def open(self) -> None:
        logger.info("RealServo %s opening (90°)", self.servo_num.name)
        self._servo.angle = 90

    def close(self) -> None:
        logger.info("RealServo %s closing (0°)", self.servo_num.name)
        self._servo.angle = 0


class FakeServo(ServoIntf):

    def __init__(self, servo_num: ServoNum) -> None:
        logger.info("Initializing FakeServo %s", servo_num.name)
        self.servo_num = servo_num

    def open(self) -> None:
        logger.info("FakeServo %s setting to 90°", self.servo_num.name)

    def close(self) -> None:
        logger.info("FakeServo %s setting to 0°", self.servo_num.name)