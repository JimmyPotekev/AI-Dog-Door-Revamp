# General
from multiprocessing import Process, Queue, Semaphore
from abc import ABC, abstractmethod
# Components
from .cv_model import CVModel
from .enums import CameraComm
# logger
from logging import getLogger

logger = getLogger(__name__)

################################################################################
# CAMERA WORKER - Performs image capturing and interfacing with the CV model   #
################################################################################
class CameraWorkerIntf(ABC):

    @abstractmethod
    def dog_in_frame(self) -> None:
        pass

    @abstractmethod
    def _get_frame(self):
        pass

    @abstractmethod
    def _process_frame(self):
        pass


class RealCameraWorker(CameraWorkerIntf):
    def __init__(self) -> None:
        logger.info("Initializing RealCameraWorker")

        self.model: CVModel = CVModel()

        logger.info("RealCameraWorker setup complete")


    def dog_in_frame(self) -> bool:
        return False


    def _get_frame(self):
        pass


    def _process_frame(self):
        pass


class FakeCameraWorker(CameraWorkerIntf):
    def __init__(self) -> None:
        logger.info("Initializing FakeCameraWorker")

        # self.model: CVModel = CVModel()

        logger.info("FakeCameraWorker setup complete")


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
    # TODO: need a way to configure RealCameraWorker or FakeCameraWorker based on mode. 
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
        
        self.in_queue: Queue = Queue(maxsize=1)
        self.out_queue = Queue()
        self.timeout_sem = Semaphore(value=0)
        self.process: Process = Process(
            target=camera_process_main,
            args=(self.in_queue, self.out_queue, self.timeout_sem),
            daemon=True
        )
        self.camera_is_on: bool = False

        logger.info("CameraManager setup complete")

# PUBLIC
    def start(self):
        self.process.start()


    def join(self):
        self.process.join()

    
    def turn_on_camera(self):
        """Turns on the camera by waking the camera process. When the camera process is on, it is continuously executing commands sent to it.
        Waits when no commands are being sent in the input queue."""
        if self.camera_is_on:
            logger.debug("Camera is already on")
            return
        self.in_queue.put(CameraComm.CAMERA_ON)
        self.camera_is_on = True


    def turn_off_camera(self):
        "Turns off the camera by putting the camera process to sleep."
        if not self.camera_is_on:
            logger.debug("Camera is already off")
            return
        self.in_queue.put(CameraComm.CAMERA_OFF)
        self.camera_is_on = False


    def is_camera_on(self) -> bool:
        return self.camera_is_on


    def dog_in_frame(self) -> bool:
        # this check may be too simple. Assumes the camera process will only ever output DOG_FOUND or NO_DOG_FOUND.
        return self.out_queue.get() == CameraComm.DOG_FOUND


    def sleep_until_timeout(self) -> None:
        # sends command for the camera process to sleep
        self.in_queue.put(CameraComm.SLEEP_TIMEOUT)


    def wait_for_timeout(self) -> None:
        # waits for the camera process to post the timeout semaphore
        self.timeout_sem.acquire()

# PRIVATE
    # These are not needed for now. They don't add anything. May expand later.
    # def _send_command(self, cmd: CameraComm):
    #     pass

    # def _get_response(self) -> CameraComm:
    #     pass
