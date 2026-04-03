import logging
from logging.handlers import RotatingFileHandler

from .settings import Settings

def configure_logging(settings: Settings) -> None:
    root_logger = logging.getLogger()

    if root_logger.handlers:
        root_logger.handlers.clear()

    if not settings.log_enabled:
        logging.disable(logging.CRITICAL)
        return

    logging.disable(logging.NOTSET)
    root_logger.setLevel(getattr(logging, settings.log_level))

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )

    # add console as log output
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(formatter)
    # root_logger.addHandler(console_handler)

    if settings.log_to_file:
        file_handler = RotatingFileHandler(
            settings.log_file,
            maxBytes=1_000_000,
            backupCount=3,
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

def clear_log_output(settings: Settings):
    with open(settings.log_file, "w") as file:
        file.write("")
