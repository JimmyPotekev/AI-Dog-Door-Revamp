# General
from time import sleep
# Components
from .config import config_system
from . import dog_door_controller as ddc
from . import dog_door_hardware as ddh

from logging import getLogger

logger = getLogger(__name__)


def main() -> None:
    config_system()

    # TODO 1) separate object initialization and pass in where needed,
    #         this supports mocks for testing(SIL & HIL) and decoupling for future hardware changes
    # TODO 2) combine into system config/setup
    # Setup system hardware and controller
    hardware = ddh.DogDoorHardware()
    controller = ddc.DogDoorController(hardware=hardware)
    

    while(True):
        # continuously update system state
        controller.update()
        # TODO: move sleep to distance sensor update & 
        sleep(1.5)

    
