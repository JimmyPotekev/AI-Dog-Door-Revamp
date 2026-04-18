# General
# Components
from .door import Door
from .sensor import SensorIntf
from .camera import CameraManager
# Enums

# logger
from logging import getLogger

logger = getLogger(__name__)

class DogDoorHardware():
    
    def __init__(self,
            door: Door,
            inside_cam: CameraManager,
            outside_cam: CameraManager,
            inside_sensor: SensorIntf,
            outside_sensor: SensorIntf):
        logger.info("Initializing Hardware")
        
        self.door = door
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
        self.door.open_doors()  


    def close_doors(self) -> None:
        self.door.close_doors()

#######################################################################
##      CAMERA OPERATIONS
#######################################################################

    def dog_in_frame(self) -> bool:
        return self.inside_cam.dog_in_frame()
    

    def turn_on_camera(self) -> None:
        self.inside_cam.turn_on_camera()


    def turn_off_camera(self) -> None:
        self.inside_cam.turn_off_camera()


    def camera_is_on(self) -> bool:
        return self.inside_cam.is_camera_on()


    def pause_camera(self) -> None:
        self.inside_cam.sleep_until_timeout()


    def wait_for_camera(self) -> None:
        self.inside_cam.wait_for_timeout()


    def shutdown(self) -> None:
        self.inside_cam.shutdown()
        self.outside_cam.shutdown()
