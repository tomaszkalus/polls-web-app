from polls_app.config import MIN_PASSWORD_LENGTH
from dataclasses import dataclass


@dataclass
class passwordValidationStatus:
    """A class to represent a password validation result with a boolean value indicating whether the password is valid and a message to display if it's not."""

    is_valid: bool
    message: str


def validate_password(
    password: str, confirm_password: str = None
) -> passwordValidationStatus:
    """Password validation method"""

    if password == "":
        return passwordValidationStatus(False, "Password cannot be empty")
    if len(password) < MIN_PASSWORD_LENGTH:
        return passwordValidationStatus(
            False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters long"
        )

    if isinstance(confirm_password, str) and confirm_password != password:
        return passwordValidationStatus(False, "Passwords don't match")

    return passwordValidationStatus(True, None)
