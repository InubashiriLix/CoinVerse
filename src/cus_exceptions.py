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
