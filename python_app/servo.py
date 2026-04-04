# Enums
from .enums import ServoNum

# logger
from logging import getLogger

logger = getLogger(__name__)

class Servo:

    def __init__(self) -> None:
        logger.info("Initializing Servo")
        logger.info("Servo setup complete")
    