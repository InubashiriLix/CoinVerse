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
