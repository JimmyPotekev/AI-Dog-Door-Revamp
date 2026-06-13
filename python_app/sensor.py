# General
from abc import ABC, abstractmethod
#Components
from gpiozero import DistanceSensor

# logger
from logging import getLogger

logger = getLogger(__name__)

class SensorIntf(ABC):
   
    @abstractmethod
    def get_distance(self) -> float:
        pass
    
    @abstractmethod
    def get_threshold(self) -> float:
        pass

class RealSensor(SensorIntf):
    def __init__(self) -> None:
        logger.info("Initializing RealSensor")
        
        # TODO: make the threshold distance a constant somewhere OR make an HLC(high level config) class that is passed around 
        # for object creation
        self.threshold = 0.5
        self.sensor: DistanceSensor = DistanceSensor(echo = 17, trigger = 4, threshold_distance = self.threshold)

        logger.info("RealSensor setup complete")
         
    def get_distance(self) -> float:
        return self.sensor.distance
    
    def get_threshold(self) -> float:
        return self.threshold
    


class FakeSensor(SensorIntf):
    def __init__(self) -> None:
        logger.info("Initializing FakeSensor")
        
        # TODO: make the threshold distance a constant somewhere OR make an HLC(high level config) class that is passed around 
        # for object creation
        self.distance = 4       # 4 meters
        self.threshold = 0.5    # 0.5 meters

        logger.info("FakeSensor setup complete")
         
    def get_distance(self) -> float:
        # this means the motion detector is triggered after 7 distance checks: (4 - 0.5) / 0.5
        self.distance -= 0.5
        self.distance = max(0, self.distance) # make sure distance is never negative
        return self.distance
    
    def get_threshold(self) -> float:
        return self.threshold