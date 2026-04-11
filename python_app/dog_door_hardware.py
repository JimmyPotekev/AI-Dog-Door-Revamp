# General
from typing import Dict
from concurrent.futures import ThreadPoolExecutor, wait
# Components
from .servo import Servo
from .sensor import Sensor
from .camera import CameraManager
# Enums
from .enums import ServoNum

# logger
from logging import getLogger

logger = getLogger(__name__)

class DogDoorHardware():
    
    def __init__(self):
        logger.info("Initializing Hardware")
        
        self.servos: Dict[ServoNum, Servo] = {
            ServoNum.SERVO1: Servo(ServoNum.SERVO1),
            ServoNum.SERVO2: Servo(ServoNum.SERVO2),
            ServoNum.SERVO3: Servo(ServoNum.SERVO3),
            ServoNum.SERVO4: Servo(ServoNum.SERVO4)
        }
        self.servo_executor = ThreadPoolExecutor(max_workers=len(self.servos))
        self.inside_sensor: Sensor = Sensor()
        self.camera: CameraManager = CameraManager()

        logger.info("Hardware setup complete")    

#######################################################################
##      SENSOR OPERATIONS
#######################################################################

    def get_distance(self) -> float:
        return self.inside_sensor.get_distance()
    
    def get_sensor_threshold(self) -> float:
        return self.inside_sensor.get_threshold()
    
#######################################################################
##      SERVO OPERATIONS
#######################################################################
    
    def open_door(self) -> None:
        logger.info("Opening Doors")

        futures = []
        for servo_num, servo in self.servos.items():
            logger.info("Opening servo #%s", servo_num.name)
            futures.append(self.servo_executor.submit(servo.open))

        wait(futures)    

        logger.info("Doors opened")       


    def close_door(self) -> None:
        logger.info("Closing Doors")

        futures = []
        for servo_num, servo in self.servos.items():
            logger.info("Closing servo #%s", servo_num.name)
            futures.append(self.servo_executor.submit(servo.close))
        
        wait(futures)

        logger.info("Doors closed")


#######################################################################
##      CAMERA OPERATIONS
#######################################################################

    def dog_in_frame(self) -> bool:
        return False
    

    def turn_on_camera(self) -> None:
        pass


    def turn_off_camera(self) -> None:
        pass
    