# General
from typing import Dict
# Components
from .servo import Servo
from .sensor import Sensor
from .camera import Camera
# Enums
from .enums import ServoNum

# logger
from logging import getLogger

logger = getLogger(__name__)

class DogDoorHardware():
    
    def __init__(self):
        logger.info("Initializing Hardware")
        
        self.servos: Dict[ServoNum, Servo] = {
            ServoNum.SERVO1: Servo(),
            ServoNum.SERVO2: Servo(),
            ServoNum.SERVO3: Servo(),
            ServoNum.SERVO4: Servo()
        }
        self.inside_sensor: Sensor = Sensor()
        self.camera: Camera = Camera()

        logger.info("Hardware setup complete")    

    def get_distance(self) -> float:
        return self.inside_sensor.get_distance()
    
    def get_sensor_threshold(self) -> float:
        return self.inside_sensor.get_threshold()