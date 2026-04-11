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
    distance_score: int = 0
    vision_count: int = 0

    # def __init__(self) -> None:
    #     logger.info("Initializing Controller")
    #     self.hardware: DogDoorHardware = DogDoorHardware()
    #     self.state: State = State.IDLE
    #     self.state_entered_at =

    #     logger.info("Controller setup complete")
        
#######################################################################
##      STATE UPDATE OPERATIONS
#######################################################################

# PUBLIC
    def update(self) -> None:
        logger.info("Upating system state")

        state_update = {
            State.IDLE: self._update_idle ,
            State.VERIFYING: self._update_verifying,
            State.OPENING: self._update_opening,
            State.OPEN: self._update_open,
            State.CLOSING: self._update_closing           
        }.get(self.state)

        # maybe should be a fault
        if state_update is None:
            logger.debug("Controller is in an UNKNOWN state")
            return
        
        state_update()


# PRIVATE
    def _update_idle(self) -> None:
        logger.info("Updating in IDLE mode")

        # take distance measurements
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
        
        # motion detected 
        # TODO don't have hard coded value
        if self.distance_score > 6: # Right now, frequency is 0.66Hz, 6 = 4 cycles. Change later
            logger.info("Motion detected in range, transitioning to VERIFYING image")
            self._exit_idle()
            self._transition_to(State.VERIFYING)
        

    def _update_verifying(self) -> None:
        logger.info("Updating in VERIFYING mode")

        # perform recognition check
        if self.hardware.dog_in_frame():
            self.vision_count += 1
        else:
            self.vision_count -= 1

        # check vision score 
        if self.vision_count >= 10: # TODO: 10 is a stand-in value. need a more accurate fequency, and not hard coded. 
            logger.info("Dog detected - transitioning to OPENING")
            self._exit_verifying(True) # keep camera on
            self._transition_to(State.OPENING)
            return
        
        time_verifying = time.monotonic() - self.state_entered_at
        if time_verifying >= self.verify_timeout_s:
            logger.info("Timeout - No dog detected, transitioning to IDLE")
            self._exit_verifying(False) #turns off camera
            self._transition_to(State.IDLE)  
            return

        # if dog detected (using score)
        #   _exit_opening (keep camera on)
        #   transition_to OPEN


    def _update_opening(self) -> None:
        logger.info("Updating in OPENING mode")


    def _update_open(self) -> None:
        logger.info("Updating in OPEN mode")

        # sleep for some timeout
        # check for dog again

        # if dog seen:
        #   reset timeout/add time
        # else:
        #   transition_to CLOSING


    def _update_closing(self) -> None:
        logger.info("Updating in CLOSING mode")

        # closes doors.
        # maybe double check to ensure camera is off.
        # transition to IDLE
        # not sure how necessary this state is.

#######################################################################
##      STATE EXIT OPERATIONS
#######################################################################

# PRIVATE

    # NOTE: may not need these separate exit functions. In _transision_to, it is already aware of the 
    #  current state of the system. It udpates the state after the appropriate exit mechanisms have been called.

    def _exit_idle(self) -> None:
        # reset distance score
        self.distance_score = 0


    def _exit_verifying(self, dog_detected: bool) -> None:
        """
            Exits the VERIFYING state. Shutdown the camera depending on if a dog was detected or not.

            Args:
                dog_detected (bool): specifies whether the VERIFYING state is exiting due to dog detection or timeout.
        """
        # reset vision count
        self.vision_count = 0
        
        # keep camera on
        if dog_detected:
            return
        
        # turn off camera if timeout
        logger.info("Turning off camera")
        self.hardware.turn_off_camera()


    def _exit_opening(self) -> None:
        pass


    def _exit_open(self) -> None:
        pass


    def _exit_closing(self) -> None:
        pass
    

    def _transition_to(self, state: State) -> None:
        """
            Performs the necessary setup to transition from the current state, to the next state.

            Args:
                state (State): The state being transitioned to.
        """
        logger.info("Transitioning from %d to %d", self.state, state)

        # setup for next state
        match state:

            case State.IDLE:
                pass
            case State.VERIFYING:
                logger.info("Turning on camera")
                self.hardware.turn_on_camera()
            case State.OPENING:
                pass
            case State.OPEN:
                pass
            case State.CLOSING:
                pass
        
        self.state = state
        self.state_entered_at = time.monotonic()
        