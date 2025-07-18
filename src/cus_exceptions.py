class TokenExpireException(Exception):
    pass


class PwdNotMatchError(Exception):
    pass


class TokenNotFoundError(Exception):
    pass


class RequireInfoLostException(Exception):
    pass


class ChangePwdError(Exception):
    pass


class EmailFormatError(Exception):
    pass


class DuplicatedAccountBookError(Exception):
    pass


class PasswordWrongError(Exception):
    pass


class TimeFormatError(Exception):
    pass


class IncomeValueError(Exception):
    """Raised when the income value is invalid."""

    pass


class IncomeTypeIndexError(Exception):
    """Raised when the income type index is invalid."""

    pass


class OutcomeValueError(Exception):
    pass


class OutcomeTypeIndexError(Exception):
    pass


class InvalidOutcomeIncomeValueError(Exception):
    """Raised when the outcome or income value is invalid."""

    pass
