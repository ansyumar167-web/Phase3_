from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from ..utils.logging_config import get_logger
import logging

logger = get_logger(__name__)

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

class ValidationError(Exception):
    """Custom exception for validation-related errors."""
    pass

class BusinessLogicError(Exception):
    """Custom exception for business logic errors."""
    pass


def handle_database_error(error: Exception, context: str = "") -> HTTPException:
    """
    Handle database errors and convert them to appropriate HTTP responses.

    Args:
        error: The exception that occurred
        context: Context information about where the error occurred

    Returns:
        HTTPException with appropriate status code and message
    """
    logger.error(f"Database error in {context}: {str(error)} (Type: {type(error).__name__})")

    if isinstance(error, SQLAlchemyError):
        return HTTPException(
            status_code=500,
            detail="A database error occurred while processing your request"
        )
    elif isinstance(error, DatabaseError):
        return HTTPException(
            status_code=503,  # Service Unavailable
            detail=str(error)
        )
    else:
        return HTTPException(
            status_code=500,
            detail=f"A database error occurred: {str(error)}"
        )


def handle_validation_error(error: Exception, context: str = "") -> HTTPException:
    """
    Handle validation errors and convert them to appropriate HTTP responses.

    Args:
        error: The exception that occurred
        context: Context information about where the error occurred

    Returns:
        HTTPException with appropriate status code and message
    """
    logger.warning(f"Validation error in {context}: {str(error)}")

    if isinstance(error, ValidationError):
        return HTTPException(
            status_code=422,  # Unprocessable Entity
            detail=str(error)
        )
    else:
        return HTTPException(
            status_code=422,
            detail=f"Validation error: {str(error)}"
        )


def handle_business_logic_error(error: Exception, context: str = "") -> HTTPException:
    """
    Handle business logic errors and convert them to appropriate HTTP responses.

    Args:
        error: The exception that occurred
        context: Context information about where the error occurred

    Returns:
        HTTPException with appropriate status code and message
    """
    logger.warning(f"Business logic error in {context}: {str(error)}")

    if isinstance(error, BusinessLogicError):
        return HTTPException(
            status_code=409,  # Conflict
            detail=str(error)
        )
    else:
        return HTTPException(
            status_code=400,  # Bad Request
            detail=f"Business logic error: {str(error)}"
        )


def safe_execute(operation, *args, **kwargs):
    """
    Safely execute an operation with proper error handling.

    Args:
        operation: The function to execute
        *args: Positional arguments to pass to the operation
        **kwargs: Keyword arguments to pass to the operation

    Returns:
        Result of the operation if successful

    Raises:
        Appropriate HTTPException based on the type of error
    """
    try:
        return operation(*args, **kwargs)
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except SQLAlchemyError as e:
        raise handle_database_error(e, f"operation: {operation.__name__}")
    except ValidationError as e:
        raise handle_validation_error(e, f"operation: {operation.__name__}")
    except BusinessLogicError as e:
        raise handle_business_logic_error(e, f"operation: {operation.__name__}")
    except Exception as e:
        logger.error(f"Unexpected error in {operation.__name__}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


def validate_user_access(user_id: str, authenticated_user_id: str) -> bool:
    """
    Validate that the authenticated user has access to the requested resource.

    Args:
        user_id: The user_id from the request
        authenticated_user_id: The authenticated user's ID

    Returns:
        True if access is granted, raises exception if not
    """
    if user_id != authenticated_user_id:
        logger.warning(f"Access denied: user {authenticated_user_id} tried to access user {user_id}'s data")
        raise HTTPException(
            status_code=403,
            detail="Access forbidden: You don't have permission to access this resource"
        )
    return True


def validate_json_payload(payload, required_fields: list = None, optional_fields: list = None):
    """
    Validate JSON payload structure.

    Args:
        payload: The payload to validate
        required_fields: List of required field names
        optional_fields: List of optional field names

    Returns:
        Validated payload

    Raises:
        ValidationError if validation fails
    """
    if required_fields is None:
        required_fields = []
    if optional_fields is None:
        optional_fields = []

    if not isinstance(payload, dict):
        raise ValidationError("Payload must be a JSON object")

    # Check for required fields
    for field in required_fields:
        if field not in payload:
            raise ValidationError(f"Required field '{field}' is missing from the request")

    # Check for unknown fields (only allow required and optional fields)
    allowed_fields = set(required_fields + optional_fields)
    provided_fields = set(payload.keys())
    unknown_fields = provided_fields - allowed_fields

    if unknown_fields:
        raise ValidationError(f"Unknown fields in request: {', '.join(unknown_fields)}")

    return payload


def setup_error_handlers(app):
    """
    Set up global error handlers for the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return {"detail": "An unexpected error occurred", "status_code": 500}

    @app.exception_handler(ValidationError)
    async def validation_exception_handler(request, exc):
        logger.warning(f"Validation error: {str(exc)}")
        return {"detail": str(exc), "status_code": 422}

    @app.exception_handler(DatabaseError)
    async def database_exception_handler(request, exc):
        logger.error(f"Database error: {str(exc)}")
        return {"detail": "A database error occurred", "status_code": 500}

    logger.info("Global error handlers configured")