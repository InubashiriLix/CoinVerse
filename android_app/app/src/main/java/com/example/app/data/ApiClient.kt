package com.example.app.data

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicReference

object ApiClient {

    /* ---------- 基础配置 ---------- */

    private val json = Json {
        ignoreUnknownKeys = true
        explicitNulls = false
    }

    private val okHttp = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .addInterceptor(
            HttpLoggingInterceptor().apply { level = HttpLoggingInterceptor.Level.BODY }
        )
        .build()

    /* ---------- Retrofit 缓存 & 动态重建 ---------- */

    private val retrofitRef = AtomicReference<Retrofit?>()

    /** 默认地址，可替换为你的内网 / 外网 */
    private const val DEFAULT_URL = "http://192.168.31.135:1919"

    /**
     * 保证拿到 **最新服务器地址** 对应的 ApiService。
     * 如果地址变了，就重建 Retrofit 实例并缓存。
     */
    private suspend fun service(): ApiService = withContext(Dispatchers.IO) {
        val baseUrl = (ServerStore.get() ?: DEFAULT_URL).trimEnd('/') + "/"

        val retrofit = retrofitRef.get()
        if (retrofit != null && retrofit.baseUrl().toString() == baseUrl) {
            retrofit.create(ApiService::class.java)
        } else {
            val newRetrofit = Retrofit.Builder()
                .baseUrl(baseUrl)
                .client(okHttp)
                .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
                .build()
            retrofitRef.set(newRetrofit)
            newRetrofit.create(ApiService::class.java)
        }
    }

    /* ---------- 对外统一调用 ---------- */

    /**
     * 协程里安全调用：
     *  - success==true        → ApiResult.Ok
     *  - success==false       → ApiResult.BizError
     *  - 网络 / 解析异常      → ApiResult.NetError
     */
    suspend fun <T> call(             // ← 删掉 inline
        block: suspend ApiService.() -> ApiEnvelope<T>
    ): ApiResult<ApiEnvelope<T>> = withContext(Dispatchers.IO) {
        try {
            val env = service().block()
            if (env.success) ApiResult.Ok(env)
            else ApiResult.BizError(env.code ?: -1, env.msg ?: "Unknown biz error")
        } catch (e: Exception) {
            ApiResult.NetError(e)
        }
    }
}