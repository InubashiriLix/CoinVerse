package com.example.app.vm


import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import com.example.app.data.TokenStore   // ⬅️ 第 3 节

class SplashVM : ViewModel() {

    private val _state = MutableStateFlow<SplashState>(SplashState.Loading)
    val state: StateFlow<SplashState> = _state

    init {
        // 模拟冷启动检查：本地有没有 token → 刷新是否成功
        viewModelScope.launch {
            val token = TokenStore.getToken()

            // 做个 800ms 动画留白（可删）
            delay(800)

            _state.value = if (token.isNullOrBlank()) {
                SplashState.ToAuth
            } else {
                SplashState.ToHome
            }
        }
    }
}
