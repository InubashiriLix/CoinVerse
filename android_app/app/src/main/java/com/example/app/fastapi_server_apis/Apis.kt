package com.example.app.fastapi_server_apis

import kotlin.collections.Map

class Apis {
    private final val testWebGate : String= "192.168.31.135:1919"
    private final val errorCodeMap: Map<Int, String> = mapOf(
        1001 to "EmailFormatError",
        1002 to "IntegrityError",
        1003 to "PwdNotMatchError",
        1004 to "TokenExpireException",
        1005 to "TokenNotFoundError",
        1006 to "RequireInfoLostException",
        1007 to "PasswordWrongError",
        1008 to "DuplicatedAccountBookError",
        1009 to "TimeFormatError",
        1010 to "IncomeValueError",
        1011 to "IncomeTypeIndexError",
        1012 to "OutcomeValueError",
        1013 to "OutcomeTypeIndexError",
        1014 to "InvalidOutcomeIncomeValueError",
        1015 to "LoginFailedError",
        1016 to "AccessDenialAccountBookError"
    )

    public fun register( username : String,   email : String): Boolean {
        return true;
    }

}