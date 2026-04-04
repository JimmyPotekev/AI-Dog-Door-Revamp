# Components
from .cv_model import CVModel
# logger
from logging import getLogger

logger = getLogger(__name__)

class Camera:
    def __init__(self) -> None:
        logger.info("Initializing Camera")

        self.model: CVModel = CVModel()

        logger.info("Camera setup complete")


    def dog_in_frame(self) -> bool:
        pass


    def get_frame(self):
        pass


    def process_frame(self):
        pass

