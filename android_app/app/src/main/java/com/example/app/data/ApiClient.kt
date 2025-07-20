package com.example.app.data

import kotlinx.serialization.json.Json
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.kotlinx.serialization.asConverterFactory
import okhttp3.MediaType.Companion.toMediaType
import java.util.concurrent.TimeUnit
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

object ApiClient {

    private val json = Json {
        ignoreUnknownKeys = true
        explicitNulls = false
    }

    private val okHttp by lazy {
        OkHttpClient.Builder()
            .connectTimeout(10, TimeUnit.SECONDS)
            .readTimeout(15, TimeUnit.SECONDS)
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            })
            .build()
    }

    private const val BASE_URL = "http://192.168.31.135:1919"

    val service: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .client(okHttp)
            .addConverterFactory(json.asConverterFactory("application/json".toMediaType()))
            .build()
            .create(ApiService::class.java)
    }

    /**
     * 协程里安全调用：
     *  - 成功 → [ApiResult.Ok] 包装完整 Envelope
     *  - 业务错误 (success=false) → [ApiResult.BizError]
     *  - 网络 / 解析异常 → [ApiResult.NetError]
     */
    suspend inline fun <T> call(
        crossinline block: suspend ApiService.() -> ApiEnvelope<T>
    ): ApiResult<ApiEnvelope<T>> = withContext(Dispatchers.IO) {
        try {
            val env = service.block()
            if (env.success) {
                ApiResult.Ok(env)
            } else {
                ApiResult.BizError(env.code ?: -1, env.msg ?: "Unknown biz error")
            }
        } catch (e: Exception) {
            ApiResult.NetError(e)
        }
    }
}
