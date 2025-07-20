package com.example.app.vm

import androidx.compose.runtime.*
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.app.data.*
import kotlinx.coroutines.launch
import com.example.app.data.ApiClient

/** 页面想要的全部状态 */
data class HomeUiState(
    val books: List<BookUi> = emptyList(),
    val isLoading: Boolean = false,
    val errorMsg: String? = null
)

class HomeVM : ViewModel() {

    /** 内部可变、外部只读 */
    private val _state = mutableStateOf(HomeUiState())
    val state: State<HomeUiState> = _state

    /** 加载账本列表 */
    fun load(token: String) = viewModelScope.launch {
        // loading → true
        _state.value = _state.value.copy(isLoading = true, errorMsg = null)

        when (val r = ApiClient.call { listBooks(ListBooksReq(token)) }) {

            is ApiResult.Ok -> {
                val booksUi = r.body.books?.map { m ->
                    val (id, tuple) = m.entries.first()
                    val (name, balance) = tuple
                    BookUi(id, name, balance)
                } ?: emptyList()

                _state.value = _state.value.copy(
                    books = booksUi,
                    isLoading = false
                )
            }

            is ApiResult.BizError -> _state.value =
                _state.value.copy(isLoading = false, errorMsg = r.msg)

            is ApiResult.NetError -> _state.value =
                _state.value.copy(isLoading = false, errorMsg = r.throwable.message)
        }
    }

    /** 调用后把错误对话框关掉 */
    fun dismissError() {
        _state.value = _state.value.copy(errorMsg = null)
    }
}
