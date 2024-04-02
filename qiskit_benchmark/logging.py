"""Everything related to logging"""

import sys
from typing import Literal

from loguru import logger as logging


def setup_logging(
    logging_level: Literal[
        "critical",
        "CRITICAL",
        "debug",
        "DEBUG",
        "error",
        "ERROR",
        "info",
        "INFO",
        "warning",
        "WARNING",
    ]
) -> None:
    """
    Sets logging format and level. The format is

        %(asctime)s [%(levelname)-8s] %(message)s

    e.g.

        2022-02-01 10:41:43,797 [INFO    ] Hello world
        2022-02-01 10:42:12,488 [CRITICAL] We're out of beans!

    Args:
        logging_level (str): Either 'critical', 'debug', 'error', 'info', or
            'warning', case insensitive.
    """
    logging.remove()
    logging.add(
        sys.stderr,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
            + "[<level>{level: <8}</level>] "
            + "<level>{message}</level>"
        ),
        level=logging_level.upper(),
        enqueue=True,
        colorize=True,
    )
