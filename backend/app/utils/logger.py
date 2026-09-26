import logging
import os
import sys


def setup_logger():
    """
    Configure the RailConnect application logger.
    """

    log_level = os.getenv(
        "LOG_LEVEL",
        "INFO"
    ).upper()

    logger = logging.getLogger("RailConnect")

    # Prevent duplicate handlers if create_app() is called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler(sys.stdout)

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    logger.propagate = False

    return logger