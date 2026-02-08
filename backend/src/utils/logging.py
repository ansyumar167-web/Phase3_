import logging
import sys
from datetime import datetime
from typing import Any, Dict
from ..config import settings


class LoggerSetup:
    """
    Centralized logger setup for the application.
    Configures logging with appropriate format, level, and handlers.
    """

    @staticmethod
    def setup_logging(name: str = __name__) -> logging.Logger:
        """
        Set up and configure a logger with the given name.

        Args:
            name: Name for the logger (defaults to module name)

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)

        # Prevent duplicate handlers if logger already exists
        if logger.handlers:
            return logger

        # Set the logging level based on configuration
        log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
        logger.setLevel(log_level)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(console_handler)

        # Prevent propagation to root logger to avoid duplicate logs
        logger.propagate = False

        return logger


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name: Name for the logger (defaults to calling module name)

    Returns:
        Configured logger instance
    """
    return LoggerSetup.setup_logging(name)


def log_exception(logger: logging.Logger, msg: str = "An exception occurred"):
    """
    Log an exception with traceback.

    Args:
        logger: Logger instance to use
        msg: Message to log with the exception
    """
    logger.exception(msg)


def log_info(logger: logging.Logger, msg: str):
    """
    Log an info message.

    Args:
        logger: Logger instance to use
        msg: Message to log
    """
    logger.info(msg)


def log_error(logger: logging.Logger, msg: str):
    """
    Log an error message.

    Args:
        logger: Logger instance to use
        msg: Message to log
    """
    logger.error(msg)


def log_warning(logger: logging.Logger, msg: str):
    """
    Log a warning message.

    Args:
        logger: Logger instance to use
        msg: Message to log
    """
    logger.warning(msg)


def log_debug(logger: logging.Logger, msg: str):
    """
    Log a debug message.

    Args:
        logger: Logger instance to use
        msg: Message to log
    """
    logger.debug(msg)