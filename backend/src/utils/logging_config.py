import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    '''
    Set up comprehensive logging configuration for the application.

    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to a log file
    '''
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s'
    )

    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        # Create logs directory if it doesn't exist
        log_path = Path(log_file).parent
        log_path.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)

    # Also configure the specific loggers for different parts of the app
    logging.getLogger('sqlalchemy').setLevel(logging.WARNING)  # Reduce SQLAlchemy noise
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('fastapi').setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    '''
    Get a named logger instance.

    Args:
        name: Name of the logger

    Returns:
        Configured logger instance
    '''
    return logging.getLogger(name)


def log_error(error: Exception, context: str = ""):
    '''
    Log an error with context information.

    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
    '''
    logger = get_logger(__name__)
    logger.error(
        f"Error in {context}: {str(error)} | Type: {type(error).__name__} | "
        f"Traceback: {getattr(error, '__traceback__', 'No traceback')}"
    )


def log_api_request(endpoint: str, method: str, user_id: Optional[str] = None,
                   status_code: Optional[int] = None, duration: Optional[float] = None):
    '''
    Log API request information for audit trail.

    Args:
        endpoint: The API endpoint that was called
        method: HTTP method used (GET, POST, etc.)
        user_id: ID of the user making the request (if authenticated)
        status_code: HTTP status code returned
        duration: Duration of the request in seconds
    '''
    logger = get_logger('api.audit')
    extra_info = []
    if user_id:
        extra_info.append(f"user_id={user_id}")
    if status_code:
        extra_info.append(f"status={status_code}")
    if duration:
        extra_info.append(f"duration={duration:.3f}s")

    extra_str = f" ({', '.join(extra_info)})" if extra_info else ""
    logger.info(f"{method} {endpoint}{extra_str}")


# Pre-configured loggers for different purposes
audit_logger = get_logger('api.audit')
error_logger = get_logger('errors')
db_logger = get_logger('database')


def configure_audit_logging():
    '''
    Set up audit logging specifically for tracking user actions and API usage.
    '''
    audit_logger.setLevel(logging.INFO)

    # Create audit log file
    audit_log_file = Path("logs") / f"audit_{datetime.now().strftime('%Y%m%d')}.log"
    audit_log_file.parent.mkdir(exist_ok=True)

    if not any(isinstance(h, logging.FileHandler) and
               h.baseFilename.endswith(audit_log_file.name) for h in audit_logger.handlers):
        audit_handler = logging.FileHandler(audit_log_file)
        audit_formatter = logging.Formatter(
            '%(asctime)s - AUDIT - %(message)s'
        )
        audit_handler.setFormatter(audit_formatter)
        audit_logger.addHandler(audit_handler)


# Initialize audit logging
configure_audit_logging()

if __name__ == "__main__":
    # Example usage
    setup_logging(log_level="INFO", log_file="logs/app.log")

    logger = get_logger("example")
    logger.info("Logging configured successfully")

    try:
        # Simulate an error
        raise ValueError("This is a test error")
    except Exception as e:
        log_error(e, "main function")
