
package com.example.app.data

sealed interface ApiResult<out T> {
    data class Ok<T>(val body: T) : ApiResult<T>
    data class BizError(val code: Int, val msg: String) : ApiResult<Nothing>
    data class NetError(val throwable: Throwable) : ApiResult<Nothing>
}
