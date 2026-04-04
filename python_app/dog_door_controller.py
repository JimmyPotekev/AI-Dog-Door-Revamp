# General
# Components
from .dog_door_hardware import DogDoorHardware
# Enums
from .enums import State
# logger
from logging import getLogger

logger = getLogger(__name__)


class DogDoorController:

    def __init__(self) -> None:
        logger.info("Initializing Controller")
        self.hardware: DogDoorHardware = DogDoorHardware()
        self.state: State = State.IDLE

        logger.info("Controller setup complete")
        

    def update(self) -> None:
        logger.info("Upating system state")



    def _update_idle(self) -> None:
        logger.info("Updating in IDLE mode")
        

    def _update_opening(self) -> None:
        logger.info("Updating in OPENING mode")


    def _update_open(self) -> None:
        logger.info("Updating in OPEN mode")


    def _update_closing(self) -> None:
        logger.info("Updating in CLOSING mode")


    def _exit_idle(self) -> None:
        # For now, IDLE has no state exit operations needed
        pass


    def _transition_to(self, state: State) -> None:
        logger.info("Transitioning from %d to %d", self.state, state)