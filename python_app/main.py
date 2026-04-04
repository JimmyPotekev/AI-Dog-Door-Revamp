# General
from time import sleep
# Components
from .config import config_system
from . import dog_door_controller as ddc

from logging import getLogger

logger = getLogger(__name__)


def main() -> None:
    config_system()

    # Create Dog Door Controller 
    controller = ddc.DogDoorController()
    

    while(True):
        # continuously update system state
        controller.update()
        sleep(1.5)

    
