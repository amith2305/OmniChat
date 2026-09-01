"""Logging setup using Python's built-in logging module."""
import logging
import sys

LOGGER_NAME = "omnichat"
_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False
    return logger
