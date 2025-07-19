import re
from datetime import datetime

from cus_exceptions import TimeFormatError


def verify_email_format(email: str) -> bool:
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def str_to_datetime(datetime_str: str) -> datetime:
    """
    Convert a string to a datetime object.
    Accepts strings like '2025-07-19T00:08:56.515468' or without microseconds.
    """
    if datetime_str.endswith("Z"):
        datetime_str = datetime_str[:-1]
    try:
        return datetime.fromisoformat(datetime_str)
    except ValueError:
        for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
            try:
                return datetime.strptime(datetime_str, fmt)
            except ValueError:
                continue
        raise TimeFormatError(
            f"timestamp str '{datetime_str}' can not be parsed as datetime"
        )


if __name__ == "__main__":
    print(verify_email_format("s@gmail.comfads@gmail.com"))
