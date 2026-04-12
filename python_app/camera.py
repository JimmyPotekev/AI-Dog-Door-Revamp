# General
from multiprocessing import Process, Queue
# Components
from .cv_model import CVModel
from .enums import CameraComm
# logger
from logging import getLogger

logger = getLogger(__name__)

################################################################################
# CAMERA WORKER - Performs image capturing and interfacing with the CV model   #
################################################################################

class CameraWorker:
    def __init__(self) -> None:
        logger.info("Initializing Camera")

        self.model: CVModel = CVModel()

        logger.info("Camera setup complete")


    def dog_in_frame(self) -> bool:
        return False


    def _get_frame(self):
        pass


    def _process_frame(self):
        pass

################################################################################
# CAMERA PROCESS MAIN - Main process for camera and cv work
#################################################################################

def camera_process_main(in_queue: Queue, out_queue: Queue) -> None:
    camera = CameraWorker()

    while True:
        cmd = in_queue.get()

        match cmd:
            case CameraComm.CAPTURE_IMG:
                dog_found = camera.dog_in_frame()
                msg = CameraComm.DOG_FOUND if dog_found else CameraComm.NO_DOG_FOUND
                out_queue.put(msg)

            case CameraComm.SHUTDOWN:
                # TODO: perform camera shutdown
                break

################################################################################
# CAMERA MANAGER - Wrapper class for communicating with the camera process     #
################################################################################

class CameraManager:
    def __init__(self) -> None:
        logger.info("Initializing CameraManager")
        
        self.in_queue: Queue = Queue()
        self.out_queue = Queue()
        self.process: Process = Process(
            target=camera_process_main,
            args=(self.in_queue, self.out_queue),
            daemon=True
        )
        # TODO: add camera_is_on attribute

        logger.info("CameraManager setup complete")

# PUBLIC
    def start(self):
        self.process.start()


    def join(self):
        self.process.join()

    
    def turn_on_camera(self):
        # debug log if camera is already on
        pass


    def turn_off_camera(self):
        # debug log if camera is already off
        pass

    def is_camera_on(self) -> bool:
        return False


    def dog_in_frame(self) -> bool:
        pass


    def sleep_until_timeout(self) -> None:
        pass


    def wait_for_timeout(self) -> None:
        pass

# PRIVATE

    def _send_command(self, cmd: CameraComm):
        pass


    def _get_response(self) -> CameraComm:
        pass