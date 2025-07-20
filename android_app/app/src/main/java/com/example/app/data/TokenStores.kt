package com.example.app.data


import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * 这里先用 MMKV / SharedPreferences 占位，
 * 后面想换 DataStore 直接改实现即可。
 */
object TokenStore {
    private var cached: String? = null

    /** 持久化到内存（示例用 Preference，自己替换） */
    suspend fun saveToken(token: String?) = withContext(Dispatchers.IO) {
        cached = token
        // TODO: 写入 DataStore / MMKV
    }

    /** 读取；冷启动时先查缓存，没有就去磁盘 */
    suspend fun getToken(): String? = withContext(Dispatchers.IO) {
        cached ?: run {
            // TODO: 读取 DataStore / MMKV
            null
        }
    }

    suspend fun clear() = saveToken(null)
}
