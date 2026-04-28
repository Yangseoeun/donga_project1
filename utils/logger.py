"""Application logger factory."""

import logging
import os


def get_logger(name: str) -> logging.Logger:
    """
    Create a configured logger.

    Args:
        name (str): Logger name.

    Returns:
        logging.Logger: Configured logger.
    """
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
    return logging.getLogger(name)
