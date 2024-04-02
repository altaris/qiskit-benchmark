"""CLI module"""

import os

import click
from loguru import logger as logging

from .logging import setup_logging


@click.command()
@click.option(
    "--logging-level",
    default=os.getenv("LOGGING_LEVEL", "info"),
    help=("Logging level, case insensitive"),
    type=click.Choice(
        ["critical", "debug", "error", "info", "warning"],
        case_sensitive=False,
    ),
)
@logging.catch
def main(logging_level: str):
    """Entrypoint."""
    setup_logging(logging_level)


# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    main()
