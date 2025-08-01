"""Set up and return a configured logger instance."""

import logging
import sys


def setup_logger(name: str = "rss_parser") -> logging.Logger:
    """Create a logger with the given name, set to DEBUG level,.

    and output formatted logs to stdout.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
