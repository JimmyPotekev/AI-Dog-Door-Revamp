from .config import config_system
from . import dog_door_controller as ddc

from logging import getLogger

logger = getLogger(__name__)


def main() -> None:
    config_system()
    
    # logg testing
    logger.info("Log message word")
    logger.warning("warning message")

    # controller testing
    controller = ddc.DogDoorController()
    controller.log()

    
