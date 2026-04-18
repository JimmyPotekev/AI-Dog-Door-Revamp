from __future__ import annotations

import logging
from dataclasses import dataclass
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from multiprocessing import Queue

from .settings import Settings

@dataclass(frozen=True)
class LoggingRuntime:
    log_queue: Queue | None
    queue_listener: QueueListener | None


def _build_handlers(settings: Settings) -> list[logging.Handler]:
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(processName)s:%(name)s] %(message)s"
    )
    handlers: list[logging.Handler] = []

    if settings.log_to_file:
        file_handler = RotatingFileHandler(
            settings.log_file,
            maxBytes=1_000_000,
            backupCount=3,
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    return handlers


def configure_main_logging(settings: Settings) -> LoggingRuntime:
    root_logger = logging.getLogger()

    if root_logger.handlers:
        root_logger.handlers.clear()

    if not settings.log_enabled:
        logging.disable(logging.CRITICAL)
        return LoggingRuntime(log_queue=None, queue_listener=None)

    logging.disable(logging.NOTSET)
    root_logger.setLevel(getattr(logging, settings.log_level))
    root_logger.propagate = False

    log_queue: Queue = Queue()
    handlers = _build_handlers(settings)
    queue_listener = QueueListener(log_queue, *handlers, respect_handler_level=True)
    queue_listener.start()
    root_logger.addHandler(QueueHandler(log_queue))

    return LoggingRuntime(log_queue=log_queue, queue_listener=queue_listener)


def configure_worker_logging(settings: Settings, log_queue: Queue | None) -> None:
    root_logger = logging.getLogger()

    if root_logger.handlers:
        root_logger.handlers.clear()

    if not settings.log_enabled or log_queue is None:
        logging.disable(logging.CRITICAL)
        return

    logging.disable(logging.NOTSET)
    root_logger.setLevel(getattr(logging, settings.log_level))
    root_logger.propagate = False
    root_logger.addHandler(QueueHandler(log_queue))


def stop_logging(runtime: LoggingRuntime) -> None:
    if runtime.queue_listener is not None:
        runtime.queue_listener.stop()

def clear_log_output(settings: Settings) -> None:
    if not settings.log_to_file:
        return

    with open(settings.log_file, "w", encoding="utf-8") as file:
        file.write("")
