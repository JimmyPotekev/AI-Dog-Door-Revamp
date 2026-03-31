from logging import getLogger

logger = getLogger(__name__)


class DogDoorController:

    def log(self):
        logger.info("hello from DogDoorController")