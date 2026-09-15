"""
Validation helpers for the web app.

Unlike the original CLI version's get_non_empty_input() / get_valid_email()
(which looped on input() until valid), these simply check a value that has
already been submitted via a form and return an error message string, or
None if the value is valid. Routes collect these into a list and re-render
the form with all errors at once if any are present.
"""

import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^\+?\d{7,15}$")


def require_non_empty(value, field_name):
    if value is None or str(value).strip() == "":
        return f"{field_name} is required."
    return None


def require_positive_integer(value, field_name):
    try:
        if int(value) <= 0:
            return f"{field_name} must be a positive number."
    except (TypeError, ValueError):
        return f"{field_name} must be a whole number."
    return None


def require_valid_email(value, field_name="Email"):
    if not value or not EMAIL_RE.match(value.strip()):
        return f"{field_name} is not a valid email address."
    return None


def require_valid_phone(value, field_name="Phone"):
    if not value or not PHONE_RE.match(value.strip()):
        return f"{field_name} must be 7-15 digits, optionally starting with +."
    return None
