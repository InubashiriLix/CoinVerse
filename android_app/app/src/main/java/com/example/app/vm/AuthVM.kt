package com.example.app.vm

import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.app.data.*          // ← ApiClient, ApiResult, LoginReq…
import com.example.app.data.TokenStore

import kotlinx.coroutines.launch
import java.security.MessageDigest
import java.util.*

class AuthVM : ViewModel() {

    val loading = mutableStateOf(false)
    val error = mutableStateOf<String?>(null)

    /**
     * 登录
     * @param onSuccess 登录成功后回调（在 ViewModel scope，UI 层直接调用）
     */
    fun login(emailOrName: String, plainPwd: String, onSuccess: () -> Unit) {
        if (loading.value) return          // 避免重复点击

        viewModelScope.launch {
            loading.value = true
            error.value = null

            // 👉 后端期待 pwd_hash，这里简单做 SHA‑256；你可以换成你后端一致的算法
            val pwdHash = sha256(plainPwd)

            when (val r = ApiClient.call {
                login(
                    LoginReq(
                        name_or_email = emailOrName,
                        pwd_hash = pwdHash,
                        maintain_online = true
                    )
                )
            }) {
                is ApiResult.Ok -> {
                    val token = r.body.accessToken
                    // 把 token 存本地，供后续接口使用
                    TokenStore.saveToken(token)
                    loading.value = false
                    onSuccess()
                }

                is ApiResult.BizError -> {
                    loading.value = false
                    error.value = r.msg
                }

                is ApiResult.NetError -> {
                    loading.value = false
                    error.value = r.throwable.message
                }
            }
        }
    }

    /* ---------------- 注册 ---------------- */
    fun register(name: String, email: String, plainPwd: String, onSuccess: () -> Unit) {
        if (loading.value) return
        viewModelScope.launch {
            loading.value = true; error.value = null
            val pwdHash = sha256(plainPwd)

            when (val r = ApiClient.call {
                register(RegisterReq(name = name, email = email, pwd_hash = pwdHash))
            }) {
                is ApiResult.Ok -> {
                    loading.value = false; onSuccess()
                }

                is ApiResult.BizError -> {
                    loading.value = false; error.value = r.msg
                }

                is ApiResult.NetError -> {
                    loading.value = false; error.value = r.throwable.message
                }
            }
        }
    }

    fun loginWithServer(
        serverUrl: String,
        emailOrName: String,
        plainPwd: String,
        onSuccess: () -> Unit
    ) = viewModelScope.launch {
        ServerStore.save(serverUrl.trimEnd('/'))   // 持久化
        login(emailOrName, plainPwd, onSuccess)    // 调用已有 login()
    }

    /** 最粗暴的 SHA‑256 -> hex */
    private fun sha256(src: String): String =
        MessageDigest.getInstance("SHA-256")
            .digest(src.toByteArray())
            .joinToString("") { "%02x".format(it) }
}


