import logging
from typing import Optional, Union

logger = logging.getLogger(__name__)


def normalize_query_param(value: Optional[str], param_name: str = "") -> Optional[str]:
    """
    Cleans and standardizes a query parameter.

    Converts values such as 'None', 'null', 'undefined', or empty strings to None.
    Trims leading/trailing whitespace.

    Args:
        value (Optional[str]): The input query parameter to normalize.
        param_name (str): Optional name of the parameter for logging context.

    Returns:
        Optional[str]: Normalized string or None if considered invalid.
    """
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned or cleaned.lower() in {"none", "null", "undefined"}:
        return None
    return cleaned


def normalize_numeric_param(
    value: Optional[Union[str, float]], param_name: str = ""
) -> Optional[float]:
    """
    Normalizes numeric input from query parameters.

    Handles conversion from string to float, ignoring values like 'null', 'undefined', or empty strings.
    Logs a warning if conversion fails.

    Args:
        value (Optional[Union[str, float]]): The numeric value (possibly as a string) to normalize.
        param_name (str): Optional name of the parameter for logging.

    Returns:
        Optional[float]: The normalized float value, or None if invalid.
    """
    if value is None:
        return None
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned or cleaned.lower() in {"none", "null", "undefined"}:
            return None
        try:
            return float(cleaned)
        except ValueError:
            logger.warning(f"Invalid numeric value for {param_name}: '{cleaned}'")
            return None
    return float(value)


def normalize_city(raw: Optional[str]) -> Optional[str]:
    """
    Extracts and normalizes a city name from a raw location string.

    Handles formats like "Chicago, IL" → "chicago".
    Returns None for empty or invalid values (e.g. "null", "undefined").

    Args:
        raw (Optional[str]): The raw input string containing the city.

    Returns:
        Optional[str]: The cleaned, lowercase city name or None if invalid.
    """
    if not raw or raw.lower() in {"none", "null", "undefined"}:
        return None
    city = raw.split(",", 1)[0].strip().lower()
    return city
