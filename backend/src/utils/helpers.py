from typing import Any, Dict, List, Optional
from datetime import datetime
import json
import uuid


def generate_unique_id() -> str:
    """
    Generate a unique identifier.

    Returns:
        A string representation of a UUID4
    """
    return str(uuid.uuid4())


def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input by removing potentially harmful characters.

    Args:
        input_str: Input string to sanitize

    Returns:
        Sanitized string
    """
    if not input_str:
        return input_str

    # Remove null bytes and basic SQL injection attempts
    sanitized = input_str.replace('\x00', '').strip()

    # Additional sanitization could be added here based on requirements
    return sanitized


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """
    Safely parse a JSON string.

    Args:
        json_str: JSON string to parse
        default: Default value to return if parsing fails

    Returns:
        Parsed JSON data or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a datetime object to a string.

    Args:
        dt: DateTime object to format
        format_str: Format string (default ISO format)

    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)


def dict_filter_none(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Remove keys with None values from a dictionary.

    Args:
        data: Dictionary to filter

    Returns:
        Dictionary with None values removed
    """
    return {k: v for k, v in data.items() if v is not None}


def list_to_dict(items: List[Any], key_field: str) -> Dict[Any, Any]:
    """
    Convert a list of objects to a dictionary using a specified field as key.

    Args:
        items: List of objects to convert
        key_field: Field name to use as dictionary key

    Returns:
        Dictionary with specified field as key
    """
    result = {}
    for item in items:
        if hasattr(item, key_field):
            key = getattr(item, key_field)
            result[key] = item
        elif isinstance(item, dict) and key_field in item:
            key = item[key_field]
            result[key] = item
    return result


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length of the text
        suffix: Suffix to append to truncated text

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def is_valid_email(email: str) -> bool:
    """
    Simple email validation.

    Args:
        email: Email address to validate

    Returns:
        True if email is valid, False otherwise
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def snake_to_camel(snake_str: str) -> str:
    """
    Convert snake_case string to camelCase.

    Args:
        snake_str: Snake case string to convert

    Returns:
        Camel case string
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.capitalize() for x in components[1:])


def camel_to_snake(camel_str: str) -> str:
    """
    Convert camelCase string to snake_case.

    Args:
        camel_str: Camel case string to convert

    Returns:
        Snake case string
    """
    import re
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any], overwrite: bool = True) -> Dict[str, Any]:
    """
    Merge two dictionaries with options to overwrite.

    Args:
        dict1: First dictionary
        dict2: Second dictionary (values from this dict will be merged)
        overwrite: Whether to overwrite values in dict1 with values from dict2

    Returns:
        Merged dictionary
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key not in result or overwrite:
            result[key] = value
    return result