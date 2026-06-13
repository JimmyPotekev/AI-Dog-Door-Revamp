# door.py
from typing import Dict, Sequence
from .servo import ServoIntf
from .enums import ServoNum
from logging import getLogger

logger = getLogger(__name__)


class Door:

    def __init__(self, servos: Sequence[ServoIntf]) -> None:
        logger.info("Initializing Door")

        self.servos: Dict[ServoNum, ServoIntf] = {
            ServoNum.SERVO1: servos[0],
            ServoNum.SERVO2: servos[1],
            ServoNum.SERVO3: servos[2],
            ServoNum.SERVO4: servos[3],
        }

        logger.info("Door setup complete")

    def open_doors(self) -> None:
        logger.info("Opening Doors")
        for servo_num, servo in self.servos.items():
            logger.info("Opening servo %s", servo_num.name)
            servo.open()
        logger.info("Doors opened")

    def close_doors(self) -> None:
        logger.info("Closing Doors")
        for servo_num, servo in self.servos.items():
            logger.info("Closing servo %s", servo_num.name)
            servo.close()
        logger.info("Doors closed")