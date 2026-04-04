#Components
from gpiozero import DistanceSensor

# logger
from logging import getLogger

logger = getLogger(__name__)

class Sensor:
    def __init__(self) -> None:
        logger.info("Initializing Sensor")
        
        # TODO: make the threshold distance a constant somewhere OR make an HLC(high level config) class that is passed around 
        # for object creation
        self.threshold = 0.5
        self.sensor: DistanceSensor = DistanceSensor(echo = 17, trigger = 4, threshold_distance = self.threshold)

        logger.info("Sensor setup complete")
         

    def get_distance(self) -> float:
        return self.sensor.distance
    
    def get_threshold(self) -> float:
        return self.threshold