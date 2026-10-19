"""Input validation for appointment requests.

Messages are written in plain English because they are shown directly to
residents (GOV.UK Service Standard point 5: make sure everyone can use
the service).
"""
import datetime as dt
import re

MAX_DAYS_AHEAD = 28

NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z '\-]{1,59}$")
# Simplified UK postcode format, e.g. "LS1 4AP", "SW1A 1AA", "M1 1AE".
POSTCODE_PATTERN = re.compile(r"^[A-Z]{1,2}[0-9][A-Z0-9]? ?[0-9][A-Z]{2}$")


class ValidationError(ValueError):
    """Raised when a request cannot be accepted; the message is resident-facing."""


def validate_name(name):
    name = (name or "").strip()
    if not NAME_PATTERN.match(name):
        raise ValidationError("Please enter your full name")
    return name


def validate_postcode(postcode):
    postcode = (postcode or "").strip().upper()
    if not POSTCODE_PATTERN.match(postcode):
        raise ValidationError("Please enter a valid UK postcode")
    return postcode


def validate_service(service, slots):
    if service not in slots:
        raise ValidationError("Please choose an available service")
    return service


def validate_date(date_text, today):
    try:
        date = dt.date.fromisoformat(date_text)
    except (TypeError, ValueError):
        raise ValidationError("Please enter the date as YYYY-MM-DD") from None
    if date < today:
        raise ValidationError("Appointments cannot be booked in the past")
    if date.weekday() >= 5:
        raise ValidationError("Appointments are only available Monday to Friday")
    if (date - today).days > MAX_DAYS_AHEAD:
        raise ValidationError(
            f"Appointments can only be booked up to {MAX_DAYS_AHEAD} days ahead")
    return date


def validate_time(time, published_times):
    if time not in published_times:
        raise ValidationError("Please choose one of the available times")
    return time
