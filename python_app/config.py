# General
import argparse
import os

from . import log_setup
from .settings import Settings

# Components
from .dog_door_hardware import DogDoorHardware
from .sensor import SensorIntf, FakeSensor, RealSensor
from .camera import CameraManagerIntf, FakeCameraManager, RealCameraManager
from .servo import ServoIntf, FakeServo, RealServo
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

def config_system() -> None:
    # logging
    settings = get_settings()
    log_setup.configure_logging(settings)
    log_setup.clear_log_output(settings)

def hardware_factory() -> DogDoorHardware:
    settings = get_settings()
    if settings.mode == "prod":
        return build_prod_system()
    else:
        return build_test_system()
    
def build_test_system() -> DogDoorHardware:
    # NOTE: not sure what the lifetime of door or other components will be here. may not persist outside this function
    door = Door([FakeServo(ServoNum.SERVO1),
                 FakeServo(ServoNum.SERVO2),
                 FakeServo(ServoNum.SERVO3),
                 FakeServo(ServoNum.SERVO4)])
    return DogDoorHardware(
        door=door,
        inside_cam = FakeCameraManager(),
        outside_cam = FakeCameraManager(),
        inside_sensor = FakeSensor(),
        outside_sensor = FakeSensor()   
    )


def build_prod_system() -> DogDoorHardware:
    # NOTE: not sure what the lifetime of door or other components will be here. may not persist outside this function
    door = Door([RealServo(ServoNum.SERVO1),
                 RealServo(ServoNum.SERVO2),
                 RealServo(ServoNum.SERVO3),
                 RealServo(ServoNum.SERVO4)])
    return DogDoorHardware(
        door = door,
        inside_cam = RealCameraManager(),
        outside_cam = RealCameraManager(),
        inside_sensor = RealSensor(),
        outside_sensor = RealSensor()
    )
