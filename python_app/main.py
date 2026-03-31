from enum import Enum, auto
from config import get_settings
from log_setup import configure_logging
from logging import getLogger
from dog_door_controller import DogDoorController

# class State(Enum)
#     IDLE = auto()
#     VERIFYING = auto()
#     OPENING = auto()
#     OPEN = auto()
#     CLOSING = auto()

# should be put into config.py, add config for devices
def sys_config():
    settings = get_settings()
    configure_logging(settings)

logger = getLogger(__name__)

def main():
    logger.info("Log message word")
    logger.warning("warning message")
    controller = DogDoorController()
    controller.log()

if __name__ == "__main__":
    sys_config()
    main()