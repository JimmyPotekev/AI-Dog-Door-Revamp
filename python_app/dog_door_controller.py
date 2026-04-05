# General
from dataclasses import dataclass, field
import time
# Components
from .dog_door_hardware import DogDoorHardware
# Enums
from .enums import State
# logger
from logging import getLogger

logger = getLogger(__name__)

@dataclass
class DogDoorController:
    hardware: DogDoorHardware
    state: State = State.IDLE
    state_entered_at: float = field(default_factory=time.monotonic)
    verify_timeout_s: float = 3.0
    open_hold_s: float = 5.0
    open_until: float | None = None
    confirm_count: int = 0
    distance_score: int = 0

    # def __init__(self) -> None:
    #     logger.info("Initializing Controller")
    #     self.hardware: DogDoorHardware = DogDoorHardware()
    #     self.state: State = State.IDLE
    #     self.state_entered_at =

    #     logger.info("Controller setup complete")
        

    def update(self) -> None:
        logger.info("Upating system state")

        state_update = {
            State.IDLE: self._update_idle ,
            State.OPENING: self._update_opening,
            State.OPEN: self._update_open,
            State.CLOSING: self._update_closing           
        }.get(self.state)

        if state_update is None:
            logger.debug("Controller is in an UNKNOWN state")
            return
        
        state_update()


    def _update_idle(self) -> None:
        logger.info("Updating in IDLE mode")

        distance = self.hardware.get_distance()
        threshold = self.hardware.get_sensor_threshold()

        logger.info("Sensor Distance: %f", distance)

        # update distance score
        if distance < threshold:
            self.distance_score += 1
        else:
            self.distance_score -= 1
            self.distance_score = max(self.distance_score, 0)

        logger.info("Distance score: %f", self.distance_score)
        # TODO don't have hard coded value
        if self.distance_score > 6: # Right now, frequency is 0.66Hz, 6 = 4 cycles. Change later
            logger.info("Motion detected in range, transitioning to VERIFYING image")
            self._exit_idle()
            self._transition_to(State.VERIFYING)
        

    def _update_opening(self) -> None:
        logger.info("Updating in OPENING mode")


    def _update_open(self) -> None:
        logger.info("Updating in OPEN mode")


    def _update_closing(self) -> None:
        logger.info("Updating in CLOSING mode")

    def _exit_idle(self) -> None:
        self.distance_score = 0


    def _transition_to(self, state: State) -> None:
        logger.info("Transitioning from %d to %d", self.state, state)