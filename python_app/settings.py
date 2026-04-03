from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    mode: str
    log_enabled: bool
    log_level: str
    log_to_file: bool
    log_file: str
