package com.example.app.data

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ApiEnvelope<T>(
    val success: Boolean,
    val msg: String? = null,
    val code: Int? = null,
    @SerialName("access_token") val accessToken: String? = null,
    val books: List<Map<Int, Pair<String, Float>>>? = null,
    val transactions: List<Map<Int, Triple<String, String?, Float>>>? = null,
    val data: T? = null,
)
