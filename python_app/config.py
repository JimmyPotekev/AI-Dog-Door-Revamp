import argparse
import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    mode: str
    log_enabled: bool
    log_level: str
    log_to_file: bool
    log_file: str

def get_settings() -> Settings:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["prod", "debug", "test"], default=None)
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default=None)
    parser.add_argument("--log-file", default=None)

    args = parser.parse_args()

    mode = args.mode or os.getenv("APP_MODE", "prod")

    if mode == "prod":
        default_log_enabled = False
        default_log_level = "WARNING"
    elif mode == "debug":
        default_log_enabled = True
        default_log_level = "DEBUG"
    else:  # test
        default_log_enabled = True
        default_log_level = "INFO"

    log_enabled = os.getenv("LOG_ENABLED")
    if log_enabled is None:
        final_log_enabled = default_log_enabled
    else:
        final_log_enabled = log_enabled == "1"

    final_log_level = args.log_level or os.getenv("LOG_LEVEL", default_log_level)
    log_file = args.log_file or os.getenv("LOG_FILE", "dogdoor.log")

    return Settings(
        mode=mode,
        log_enabled=final_log_enabled,
        log_level=final_log_level,
        log_to_file=final_log_enabled,
        log_file=log_file,
    )