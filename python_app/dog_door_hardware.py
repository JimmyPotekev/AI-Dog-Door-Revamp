# General
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, wait
# Components
from .servo import ServoIntf
from .sensor import SensorIntf
from .camera import CameraManagerIntf
# Enums
from .enums import ServoNum

# logger
from logging import getLogger

logger = getLogger(__name__)

class DogDoorHardware():
    
    def __init__(self,
            servos: List[ServoIntf],
            inside_cam: CameraManagerIntf,
            outside_cam: CameraManagerIntf,
            inside_sensor: SensorIntf,
            outside_sensor: SensorIntf):
        logger.info("Initializing Hardware")
        
        self.servos: Dict[ServoNum, ServoIntf] = {
            ServoNum.SERVO1: servos[0],
            ServoNum.SERVO2: servos[1],
            ServoNum.SERVO3: servos[2],
            ServoNum.SERVO4: servos[3]
        }
        self.servo_executor = ThreadPoolExecutor(max_workers=len(self.servos))
        self.inside_cam = inside_cam
        self.outside_cam = outside_cam
        self.inside_sensor = inside_sensor
        self.outside_sensor = outside_sensor

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


#######################################################################
##      CAMERA OPERATIONS
#######################################################################

    def dog_in_frame(self) -> bool:
        return self.inside_cam.dog_in_frame()
    

    def turn_on_camera(self) -> None:
        self.inside_cam.turn_on_camera()


    def turn_off_camera(self) -> None:
        self.inside_cam.turn_on_camera()


    def camera_is_on(self) -> bool:
        return self.inside_cam.is_camera_on()


    def pause_camera(self) -> None:
        self.inside_cam.sleep_until_timeout()


    def wait_for_camera(self) -> None:
        self.inside_cam.wait_for_timeout()