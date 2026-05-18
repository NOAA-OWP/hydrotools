"""Utilities for validating and transforming datetime arguments."""
from datetime import datetime, timedelta, UTC
from typing import TypeAlias, Union, Literal, Sequence, Annotated
import pandas as pd
from pydantic import BeforeValidator

DateTimeObject: TypeAlias = Union[datetime, pd.Timestamp]
"""Type alias for date+time objects."""

DurationObject: TypeAlias = Union[timedelta, pd.Timedelta]
"""Type alias for time duration objects."""

TimeInterval: TypeAlias = Sequence[DateTimeObject | None]
"""Type alias for a bounded or half-bounded time interval."""

DateTimeInput: TypeAlias = Union[DateTimeObject, DurationObject, TimeInterval]
"""Type alias for objects compatible with datetime arguments."""

def convert_datetime_to_string(
        datetime_object: DateTimeInput,
        timespec: Literal['auto', 'hours', 'minutes', 'seconds', 'milliseconds',
            'microseconds', 'nanoseconds'] = "seconds"
) -> str:
    """Converts a datetime-like or duration-like object to a standardized RFC 3339
    string in UTC.
    
    Args:
        datetime_object: A datetime, timedelta, or sequence of datetime compatible
            objects to convert (e.g. [start, end]).
        timespec: Maximum precision of datetime strings. Defaults to "seconds".
    
    Returns:
        A date-time or interval string, adhering to RFC 3339 format. Intervals may be 
        bounded or half-bounded (double-dots at start or end). Duration objects
        like timedelta or pandas.Timedelta are converted to an equivalent bounded
        interval ending at the current time.

    Example:
    >>> # Single datetime object conversion
    >>> convert_datetime_to_string(datetime(2025, 1, 3))
    ... "2025-01-03T00:00:00+00:00"

    >>> # Timedelta conversion, assuming current time is 2025-01-03T00:00:00+00:00
    >>> convert_datetime_to_string(timedelta(hours=36))
    ... "2025-01-01T12:00:00+00:00/2025-01-03T00:00:00+00:00"

    >>> # Sequence of datetimes
    >>> convert_datetime_to_string([datetime(2025, 2, 3), datetime(2025, 2, 5)])
    ... "2025-02-03T12:00:00+00:00/2025-02-05T00:00:00+00:00"

    >>> # Half-bounded interval
    >>> convert_datetime_to_string([None, datetime(2025, 2, 5)])
    ... "../2025-02-05T00:00:00+00:00"
    
    Raises:
        ValueError if unable to convert object to string.
    """
    # Datetime normalizer
    def normalize_datetime(dt: DateTimeObject) -> DateTimeObject:
        if dt.tzinfo:
            return dt.astimezone(UTC)
        else:
            return pd.Timestamp(dt).tz_localize(UTC)

    # Normalize object and convert to string
    if isinstance(datetime_object, DateTimeObject):
        # Normalize
        return normalize_datetime(datetime_object).isoformat(timespec=timespec)

    elif isinstance(datetime_object, DurationObject):
        # Convert to UTC datetime interval
        now = pd.Timestamp.now(UTC)
        end = normalize_datetime(now).isoformat(timespec=timespec)
        start = normalize_datetime(now - datetime_object).isoformat(timespec=timespec)
        return f"{start}/{end}"

    elif isinstance(datetime_object, Sequence):
        # Check length
        if len(datetime_object) != 2:
            raise ValueError(
                "Sequence of datetime objects must be exactly length two (e.g. [start, end])"
            )

        # Check that at least one object is not None
        if all([not d for d in datetime_object]):
            raise ValueError("Both datetime objects are None. Cannot convert unbounded interval.")

        # Check that non-None objects are actually datetime
        if any([not isinstance(d, DateTimeObject) for d in datetime_object if d]):
            raise ValueError(f"All items in {datetime_object} must be datetime-compatible")

        # Normalize
        normalized = [normalize_datetime(d) if d else d for d in datetime_object]

        # Check that start occurs before end
        if isinstance(normalized[0], DateTimeObject) and isinstance(normalized[1], DateTimeObject):
            if normalized[0] >= normalized[1]:
                raise ValueError(
                    f"Improper interval {datetime_object} ([start, end]). start must be < end."
                )

        # Normalize and convert to strings
        normalized_strings = [d.isoformat(timespec=timespec) if d else ".." for d in normalized]
        return f"{normalized_strings[0]}/{normalized_strings[1]}"

    raise ValueError(f"Cannot convert {datetime_object} to datetime string or interval string.")

def validate_datetime_argument(
        datetime_object: str | DateTimeInput
) -> str:
    """Reusable validator for datetime arguments. Note that strings are not
    validated for proper format. String arguments are left as-is to facilitate
    direct access to the API.
    """
    # Strings are not validated
    if isinstance(datetime_object, str):
        return datetime_object

    # Other types
    return convert_datetime_to_string(datetime_object)

DateTimeField: TypeAlias = Annotated[
    str,
    BeforeValidator(validate_datetime_argument)
]
"""Annotated type that validates and converts object to RFC 3339 strings.
Note that string inputs will be passed directly to the API without validation.
"""
