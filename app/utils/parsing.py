from datetime import datetime
from typing import Optional
import dateutil.parser


def safe_parse_datetime(value: Optional[str]) -> Optional[datetime]:
    """
    Safely parses a string into a datetime object.

    Supports flexible date formats like 'tomorrow', 'next Friday', '07-31-2025', etc.
    Returns None if the input is empty or invalid.

    Args:
        value (Optional[str]): A string representing a datetime.

    Returns:
        Optional[datetime]: A datetime object if parsing succeeds, otherwise None.
    """
    if not value or not value.strip():
        return None
    try:
        return dateutil.parser.parse(value)
    except (ValueError, TypeError):
        return None


def safe_parse_float(value: Optional[str]) -> Optional[float]:
    """
    Safely parses a string into a float.

    Returns None if the input is empty or invalid (non-numeric).

    Args:
        value (Optional[str]): A string representation of a float.

    Returns:
        Optional[float]: Parsed float value or None.
    """
    if not value or not value.strip():
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def safe_parse_str(value: Optional[str]) -> Optional[str]:
    """
    Safely strips a string and returns None if it's empty.

    Args:
        value (Optional[str]): The string to sanitize.

    Returns:
        Optional[str]: A non-empty, stripped string or None.
    """
    return value.strip() if value and value.strip() else None
