"""Everything related to logging"""

import sys

from loguru import logger as logging


def setup_logging(level: str) -> None:
    """
    Sets logging format and level. The format is

        %(asctime)s [%(levelname)-8s] %(message)s

    e.g.

        2022-02-01 10:41:43,797 [INFO    ] Hello world
        2022-02-01 10:42:12,488 [CRITICAL] We're out of beans!

    Args:
        level (str): Either 'critical', 'debug', 'error', 'info', or
            'warning', case insensitive.
    """
    if level.lower() not in [
        "critical",
        "debug",
        "error",
        "info",
        "warning",
    ]:
        level = "info"
    logging.remove()
    logging.add(
        sys.stderr,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> "
            + "[<level>{level: <8}</level>] "
            + "<level>{message}</level>"
        ),
        level=level.upper(),
        enqueue=True,
        colorize=True,
    )
