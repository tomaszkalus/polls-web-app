from sqids import Sqids
from .config import MIN_URL_STRING_LENGTH


def generate_url_identifier(_id: int) -> str:
    """Generates a url identifier for a poll based on its id"""
    return Sqids(min_length=MIN_URL_STRING_LENGTH).encode(_id)


def decode_url_identifier(url_identifier: str) -> int:
    """Decodes a url identifier for a poll from hashed string into its ID"""
    return Sqids(min_length=MIN_URL_STRING_LENGTH).decode(url_identifier)[0]


def poll_name_to_filename(poll_name: str) -> str:
    """Converts a poll name into a filename"""

    chars = "-_()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    new_filename = "".join([char for char in poll_name.replace(" ","_") if char in chars])
    return new_filename
