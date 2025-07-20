package com.example.app.data

object ServerStore {
    private var cached: String? = null

    suspend fun save(url: String) {
        cached = url
        // TODO: DataStore / MMKV 持久化
    }
    suspend fun get(): String? = cached    // 同理：读 DataStore
}