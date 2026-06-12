from __future__ import annotations

# General
from multiprocessing import Process, Queue, Semaphore, Event
import queue
from abc import ABC, abstractmethod
from time import sleep
# Components
from .cv_model import CVModel
from .enums import CameraComm
from .log_setup import configure_worker_logging
from .settings import Settings
# logger
from logging import getLogger, Logger

logger = getLogger(__name__)

################################################################################
# CAMERA WORKER - Performs image capturing and interfacing with the CV model   #
################################################################################
class CameraWorkerIntf(ABC):

    @abstractmethod
    def turn_on_camera(self) -> None:
        pass

    def dog_in_frame(self) -> None:
        pass

    @abstractmethod
    def _get_frame(self):
        pass

    @abstractmethod
    def _process_frame(self):
        pass


class RealCameraWorker(CameraWorkerIntf):
    def __init__(self, camera_logger: Logger) -> None:
        logger.info("Initializing RealCameraWorker")

        self.model: CVModel = CVModel()

        logger.info("RealCameraWorker setup complete")

    def turn_on_camera(self) -> None:
        pass

    def dog_in_frame(self) -> bool:
        return False


    def _get_frame(self):
        pass


    def _process_frame(self):
        pass


class FakeCameraWorker(CameraWorkerIntf):
    def __init__(self, camera_logger: Logger) -> None:
        camera_logger.info("Initializing FakeCameraWorker")

        self.detection_attemps = 0
        self.logger = camera_logger
        self.camera_is_on = False
        # self.model: CVModel = CVModel()

        camera_logger.info("FakeCameraWorker setup complete")

    def turn_on_camera(self) -> None:
        self.logger.info("Turning on camera")
        self.camera_is_on = True

    def turn_off_camer(self) -> None:
        self.logger.info("Turning off camera")
        self.camera_is_on = False

    def dog_in_frame(self) -> bool:
        logger.info("Checking for dog")
        self.detection_attemps += 1
        
        self._get_frame()
        self._process_frame()

        if self.detection_attemps > 20:
            self.detection_attemps = 0
            return False
        if self.detection_attemps > 10:
            logger.info("DOG FOUND")
            return True
        
        return False


    def _get_frame(self):
        self.logger.info("Getting frame")


    def _process_frame(self):
        self.logger.info("Processing frame") 

################################################################################
# CAMERA PROCESS MAIN - Main process for camera and cv work
#################################################################################

def camera_process_main(
    in_queue: Queue,
    out_queue: Queue,
    run_event: Event,
    timeout_sem: Semaphore,
    idle_sem: Semaphore,
    log_queue: Queue | None,
    settings: Settings,
    use_fake_worker: bool,
) -> None:
    configure_worker_logging(settings, log_queue)

    logger.info("Starting camera process")
    camera: CameraWorkerIntf
    if use_fake_worker:
        camera = FakeCameraWorker(logger)
    else:
        camera = RealCameraWorker(logger)

    camera_is_on = False

    # Process main loop
    logger.info("Entering camera process main loop")
    while True:
        sleep(0.3)
        # Camera proccess 'idles' till idle_sem is posted by main process
        # idle_sem.acquire()
        if not run_event.is_set():
            logger.info("Camera idling...")
            run_event.wait()
            logger.info("Camera starting up...")
        
        cmd = None
        try:
            cmd = in_queue.get_nowait()
        except queue.Empty:
            logger.info("No command found")
        logger.info("Cmd: %s", cmd)

        match cmd:
            # case CameraComm.CAPTURE_IMG:
            #     # if not camera_is_on:
            #     #     logger.debug("Ignoring capture request because camera is off")
            #     #     # out_queue.put(CameraComm.NO_DOG_FOUND)
            #     #     continue
            #     dog_found = camera.dog_in_frame()
            #     msg = CameraComm.DOG_FOUND if dog_found else CameraComm.NO_DOG_FOUND
            #     out_queue.put(msg)

            # NOTE: This command seems useless, if the process is woken by semaphore post instead of the command. 
            # case CameraComm.CAMERA_ON:
            #     camera_is_on = True
            #     logger.info("Camera process enabled")
            #     camera.turn_on_camera()

            case CameraComm.CAMERA_OFF:
                camera_is_on = False
                logger.info("Camera process disabled")
                # idle_sem.aquire()
                run_event.clear()
                continue

            case CameraComm.SLEEP_TIMEOUT:
                logger.info("Camera process entering timeout sleep")
                # TODO: sleep time should not be hard coded. Somehow need to get this sleep value from the dog_dor_controller. 
                sleep(3.5)
                timeout_sem.release() #NOTE might be better as a barrier

            case CameraComm.SHUTDOWN:
                logger.info("Shutting down camera process")
                break

        dog_found = camera.dog_in_frame()
        msg = CameraComm.DOG_FOUND if dog_found else CameraComm.NO_DOG_FOUND
        # NOTE maybe not the best approach to overwrite a stale result
        try:
            out_queue.put_nowait(msg)
        except queue.Full:
            # replace stale result
            try:
                out_queue.get_nowait()
            except queue.Empty:
                pass    
            out_queue.put(msg)
            
    logger.info("Camera process stopped")

################################################################################
# CAMERA MANAGER - Wrapper class for communicating with the camera process     #
################################################################################

class CameraManager:
    def __init__(
        self,
        settings: Settings,
        log_queue: Queue | None,
        use_fake_worker: bool,
        process_name: str = "CameraProcess",
    ) -> None:
        logger.info("Initializing CameraManager")
        
        self.in_queue: Queue = Queue(maxsize=1)
        self.out_queue = Queue()
        self.run_event = Event()
        self.timeout_sem = Semaphore(value=0)
        self.idle_sem = Semaphore(value=0)
        self.process_name = process_name
        self.process: Process = Process(
            target=camera_process_main,
            args=(
                self.in_queue,
                self.out_queue,
                self.run_event,
                self.timeout_sem,
                self.idle_sem,
                log_queue,
                settings,
                use_fake_worker,
            ),
            name=process_name,
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
        # self.in_queue.put(CameraComm.CAMERA_ON)
        
        # post idle_sem for camera process to resume execution
        # self.idle_sem.release() 
        self.run_event.set()
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
        # self.in_queue.put(CameraComm.CAPTURE_IMG)
        return self.out_queue.get() == CameraComm.DOG_FOUND


    def sleep_until_timeout(self) -> None:
        # sends command for the camera process to sleep
        self.in_queue.put(CameraComm.SLEEP_TIMEOUT)


    def wait_for_timeout(self) -> None:
        # waits for the camera process to post the timeout semaphore
        self.timeout_sem.acquire()


    def shutdown(self) -> None:
        # Signals the camera process to exit
        if not self.process.is_alive():
            return

        self.in_queue.put(CameraComm.SHUTDOWN)
        self.process.join(timeout=2)

        if self.process.is_alive():
            logger.warning("%s did not exit before timeout", self.process_name)

# PRIVATE
    # These are not needed for now. They don't add anything. May expand later.
    # def _send_command(self, cmd: CameraComm):
    #     pass

    # def _get_response(self) -> CameraComm:
    #     pass
