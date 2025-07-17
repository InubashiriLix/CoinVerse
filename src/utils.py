import re
from datetime import datetime


def verify_email_format(email: str) -> bool:
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def str_to_datetime(datetime_str: str) -> datetime:
    """
    Convert a string to a datetime object.

    Args:
        datetime_str (str): The string representation of the datetime.

    Returns:
        datetime: The corresponding datetime object.
    Raises:
        ValueError: If the string is not in the correct format.
    """
    return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%f")


if __name__ == "__main__":
    print(verify_email_format("s@gmail.comfads@gmail.com"))
