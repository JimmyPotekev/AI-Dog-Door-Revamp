# General
from time import sleep
# Components
from .config import config_system, hardware_factory
from . import dog_door_controller as ddc
from . import log_setup
# from . import dog_door_hardware

from logging import getLogger

logger = getLogger(__name__)


def main() -> None:
    hardware = None
    logging_runtime = None

    try:
        settings, logging_runtime = config_system()

        # TODO 1) separate object initialization and pass in where needed,
        #         this supports mocks for testing(SIL & HIL) and decoupling for future hardware changes
        # TODO 2) combine into system config/setup
        # Setup system hardware and controller
        hardware = hardware_factory(settings, logging_runtime.log_queue)
        controller = ddc.DogDoorController(hw=hardware)

        while(True):
            # continuously update system state
            controller.update()
            # TODO: move sleep to distance sensor update &
            sleep(1.5)
    except KeyboardInterrupt:
        logger.info("Shutting down application")
    finally:
        if hardware is not None:
            hardware.shutdown()

        if logging_runtime is not None:
            log_setup.stop_logging(logging_runtime)

    
