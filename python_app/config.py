from __future__ import annotations

# General
import argparse
import os
from multiprocessing import Queue

from . import log_setup
from .settings import Settings

# Components
from .dog_door_hardware import DogDoorHardware
from .sensor import FakeSensor, RealSensor
from .camera import CameraManager
from .servo import FakeServo, RealServo
from .door import Door
# Enums
from .enums import ServoNum

def get_settings() -> Settings:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["prod", "debug", "test"], default=None)
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default=None)
    parser.add_argument("--log-file", default=None)
    parser.add_argument("--log-enabled", choices=["0", "1"], default=None)

    args = parser.parse_args()

    mode = args.mode

    if mode == "prod":
        default_log_enabled = False
        default_log_level = "WARNING"
    elif mode == "debug":
        default_log_enabled = True
        default_log_level = "DEBUG"
    else:  # test
        default_log_enabled = True
        default_log_level = "INFO"

    log_enabled_arg = args.log_enabled
    if log_enabled_arg is None:
        final_log_enabled = default_log_enabled
    else:
        final_log_enabled = log_enabled_arg == "1"

    final_log_level = args.log_level or os.getenv("LOG_LEVEL", default_log_level)
    log_file = args.log_file or os.getenv("LOG_FILE", "dogdoor.log")

    return Settings(
        mode=mode,
        log_enabled=final_log_enabled,
        log_level=final_log_level,
        log_to_file=final_log_enabled,
        log_file=log_file,
    )

def config_system() -> tuple[Settings, log_setup.LoggingRuntime]:
    settings = get_settings()
    log_setup.clear_log_output(settings)
    logging_runtime = log_setup.configure_main_logging(settings)
    return settings, logging_runtime

def hardware_factory(settings: Settings, log_queue: Queue | None) -> DogDoorHardware:
    if settings.mode == "prod":
        return build_prod_system(settings, log_queue)
    else:
        return build_test_system(settings, log_queue)
    
def build_test_system(settings: Settings, log_queue: Queue | None) -> DogDoorHardware:
    # NOTE: not sure what the lifetime of door or other components will be here. may not persist outside this function
    inside_cam = CameraManager(
        settings=settings,
        log_queue=log_queue,
        use_fake_worker=True,
        process_name="InsideCameraProcess",
    )
    outside_cam = CameraManager(
        settings=settings,
        log_queue=log_queue,
        use_fake_worker=True,
        process_name="OutsideCameraProcess",
    )

    door = Door([FakeServo(s) for s in ServoNum])
    
    # Start camera processes
    inside_cam.start()
    # outside_cam.start()

    return DogDoorHardware(
        door=door,
        inside_cam = inside_cam,
        outside_cam = outside_cam,
        inside_sensor = FakeSensor(),
        outside_sensor = FakeSensor()   
    )


def build_prod_system(settings: Settings, log_queue: Queue | None) -> DogDoorHardware:
    # NOTE: not sure what the lifetime of door or other components will be here. may not persist outside this function
    door = Door(RealServo.make_servos())

    inside_cam = CameraManager(
        settings=settings,
        log_queue=log_queue,
        use_fake_worker=False,
        process_name="InsideCameraProcess",
    )
    outside_cam = CameraManager(
        settings=settings,
        log_queue=log_queue,
        use_fake_worker=False,
        process_name="OutsideCameraProcess",
    )

    # Start camear processes
    inside_cam.start()
    # outside_cam.start()

    return DogDoorHardware(
        door = door,
        inside_cam = inside_cam,
        outside_cam = outside_cam,
        inside_sensor = RealSensor(),
        outside_sensor = RealSensor()
    )
