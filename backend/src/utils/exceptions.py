from typing import Optional, Dict, Any
from fastapi import HTTPException, status
import logging


logger = logging.getLogger(__name__)


class BaseCustomException(Exception):
    """Base exception class for all custom exceptions in the application."""

    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "GENERAL_ERROR"
        self.details = details or {}

        # Log the exception
        logger.error(f"{self.__class__.__name__}: {message} (Code: {self.error_code})", extra={
            "error_code": self.error_code,
            "details": self.details
        })


class AuthenticationError(BaseCustomException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "AUTH_ERROR", details)


class AuthorizationError(BaseCustomException):
    """Raised when authorization fails (user doesn't have permission)."""

    def __init__(self, message: str = "Authorization failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "AUTHZ_ERROR", details)


class ValidationError(BaseCustomException):
    """Raised when data validation fails."""

    def __init__(self, message: str = "Validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "VALIDATION_ERROR", details)


class ResourceNotFoundError(BaseCustomException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "RESOURCE_NOT_FOUND", details)


class DatabaseError(BaseCustomException):
    """Raised when a database operation fails."""

    def __init__(self, message: str = "Database operation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "DATABASE_ERROR", details)


class BusinessLogicError(BaseCustomException):
    """Raised when business logic validation fails."""

    def __init__(self, message: str = "Business logic validation failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "BUSINESS_LOGIC_ERROR", details)


class RateLimitExceededError(BaseCustomException):
    """Raised when rate limits are exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "RATE_LIMIT_EXCEEDED", details)


class ExternalServiceError(BaseCustomException):
    """Raised when an external service call fails."""

    def __init__(self, message: str = "External service error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", details)


class ConfigurationError(BaseCustomException):
    """Raised when there's a configuration issue."""

    def __init__(self, message: str = "Configuration error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "CONFIGURATION_ERROR", details)


class TaskNotFoundException(ResourceNotFoundError):
    """
    Raised when a task is not found in the database.
    """

    def __init__(self, task_id: int, user_id: str):
        super().__init__(
            message=f"Task with ID {task_id} not found for user {user_id}",
            error_code="TASK_NOT_FOUND",
            details={"task_id": task_id, "user_id": user_id}
        )


class TaskAccessDeniedException(AuthorizationError):
    """
    Raised when a user tries to access a task they don't own.
    """

    def __init__(self, task_id: int, user_id: str):
        super().__init__(
            message=f"Access denied to task with ID {task_id} for user {user_id}",
            error_code="TASK_ACCESS_DENIED",
            details={"task_id": task_id, "user_id": user_id}
        )


class DatabaseOperationException(DatabaseError):
    """
    Raised when a database operation fails.
    """

    def __init__(self, operation: str, original_exception: Exception = None):
        super().__init__(
            message=f"Database operation '{operation}' failed",
            error_code="DATABASE_OPERATION_FAILED",
            details={
                "operation": operation,
                "original_error": str(original_exception) if original_exception else None
            }
        )


class MCPServerError(BaseCustomException):
    """
    Raised when an MCP server operation fails.
    """

    def __init__(self, tool_name: str, error_details: dict = None):
        super().__init__(
            message=f"MCP server tool '{tool_name}' execution failed",
            error_code="MCP_SERVER_ERROR",
            details={
                "tool_name": tool_name,
                "error_details": error_details or {}
            }
        )


# HTTP Exception helpers
def http_exception_400(detail: str = "Bad Request", headers: Optional[Dict[str, str]] = None):
    """Return HTTP 400 Bad Request exception."""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
        headers=headers
    )


def http_exception_401(detail: str = "Unauthorized", headers: Optional[Dict[str, str]] = None):
    """Return HTTP 401 Unauthorized exception."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers=headers
    )


def http_exception_403(detail: str = "Forbidden", headers: Optional[Dict[str, str]] = None):
    """Return HTTP 403 Forbidden exception."""
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
        headers=headers
    )


def http_exception_404(detail: str = "Not Found", headers: Optional[Dict[str, str]] = None):
    """Return HTTP 404 Not Found exception."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=detail,
        headers=headers
    )


def http_exception_409(detail: str = "Conflict", headers: Optional[Dict[str, str]] = None):
    """Return HTTP 409 Conflict exception."""
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=detail,
        headers=headers
    )


def http_exception_422(detail: str = "Unprocessable Entity", headers: Optional[Dict[str, str]] = None):
    """Return HTTP 422 Unprocessable Entity exception."""
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=detail,
        headers=headers
    )


def http_exception_429(detail: str = "Too Many Requests", headers: Optional[Dict[str, str]] = None):
    """Return HTTP 429 Too Many Requests exception."""
    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail=detail,
        headers=headers
    )


def http_exception_500(detail: str = "Internal Server Error", headers: Optional[Dict[str, str]] = None):
    """Return HTTP 500 Internal Server Error exception."""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=detail,
        headers=headers
    )


# Exception to HTTP Exception mapping
EXCEPTION_HTTP_MAP = {
    AuthenticationError: lambda e: http_exception_401(e.message),
    AuthorizationError: lambda e: http_exception_403(e.message),
    ValidationError: lambda e: http_exception_400(e.message),
    ResourceNotFoundError: lambda e: http_exception_404(e.message),
    DatabaseError: lambda e: http_exception_500(e.message),
    BusinessLogicError: lambda e: http_exception_400(e.message),
    RateLimitExceededError: lambda e: http_exception_429(e.message),
    ExternalServiceError: lambda e: http_exception_500(e.message),
    ConfigurationError: lambda e: http_exception_500(e.message),
}


def handle_app_exception(exc: BaseCustomException, logger: logging.Logger = None) -> HTTPException:
    """
    Convert a custom exception to the appropriate HTTP exception.

    Args:
        exc: The custom exception to convert
        logger: Optional logger to log the exception

    Returns:
        Appropriate HTTPException based on the custom exception type
    """
    if logger:
        logger.error(f"Application exception: {exc}", exc_info=True)

    handler = EXCEPTION_HTTP_MAP.get(type(exc))
    if handler:
        return handler(exc)

    # Default to 500 for unmapped exceptions
    return http_exception_500(str(exc))


def handle_database_exception(db_exc: Exception, operation: str, logger: logging.Logger = None) -> HTTPException:
    """
    Handle database exceptions and convert to appropriate HTTP exceptions.

    Args:
        db_exc: The database exception
        operation: The operation that caused the exception
        logger: Optional logger to log the exception

    Returns:
        HTTPException with appropriate status code and detail
    """
    db_operation_exception = DatabaseOperationException(operation, db_exc)

    if logger:
        logger.error(f"Database operation failed: {db_operation_exception}", exc_info=True)

    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "error_code": db_operation_exception.error_code,
            "message": db_operation_exception.message,
            "details": db_operation_exception.details
        }
    )


def handle_validation_exception(field: str, value: str, reason: str, logger: logging.Logger = None) -> HTTPException:
    """
    Handle validation exceptions and convert to appropriate HTTP exceptions.

    Args:
        field: The field that failed validation
        value: The value that failed validation
        reason: The reason for validation failure
        logger: Optional logger to log the exception

    Returns:
        HTTPException with appropriate status code and detail
    """
    validation_exception = ValidationError(
        message=f"Validation failed for field '{field}' with value '{value}': {reason}",
        details={
            "field": field,
            "value": value,
            "reason": reason
        }
    )

    if logger:
        logger.warning(f"Validation failed: {validation_exception}")

    return handle_app_exception(validation_exception, logger)


# Context manager for exception logging
class ExceptionLogger:
    """Context manager to log exceptions with additional context."""

    def __init__(self, operation: str, user_id: Optional[str] = None, **context):
        self.operation = operation
        self.user_id = user_id
        self.context = context

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Log the exception with context
            logger.error(
                f"Exception in {self.operation}: {exc_val}",
                extra={
                    "operation": self.operation,
                    "user_id": self.user_id,
                    **self.context
                }
            )
        return False  # Don't suppress the exception


# Decorator for automatic exception handling
def handle_exceptions(func):
    """
    Decorator to automatically handle and log exceptions in functions.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseCustomException:
            # Re-raise custom exceptions as-is
            raise
        except HTTPException:
            # Re-raise HTTP exceptions as-is
            raise
        except Exception as e:
            # Log unexpected exceptions and convert to 500 error
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}", exc_info=True)
            raise http_exception_500("An unexpected error occurred")
    return wrapper