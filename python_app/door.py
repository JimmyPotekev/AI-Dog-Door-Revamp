# General
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, wait
# Components
from .servo import ServoIntf
# Enums
from .enums import ServoNum

# logger
from logging import getLogger

logger = getLogger(__name__)


class Door:

    def __init__(self, servos: List[ServoIntf]) -> None:
        logger.info("Initializing Door")
        
        self.servos: Dict[ServoNum, ServoIntf] = {
            ServoNum.SERVO1: servos[0],
            ServoNum.SERVO2: servos[1],
            ServoNum.SERVO3: servos[2],
            ServoNum.SERVO4: servos[3]
        }

        self.servo_executor = ThreadPoolExecutor(max_workers=len(self.servos))

        logger.info("Door setup complete")  

    
    def open_doors(self) -> None:
        logger.info("Opening Doors")

        futures = []
        for servo_num, servo in self.servos.items():
            logger.info("Opening servo #%s", servo_num.name)
            futures.append(self.servo_executor.submit(servo.open))

        wait(futures)    

        logger.info("Doors opened")       


    def close_doors(self) -> None:
        logger.info("Closing Doors")

        futures = []
        for servo_num, servo in self.servos.items():
            logger.info("Closing servo #%s", servo_num.name)
            futures.append(self.servo_executor.submit(servo.close))
        
        wait(futures)

        logger.info("Doors closed")

