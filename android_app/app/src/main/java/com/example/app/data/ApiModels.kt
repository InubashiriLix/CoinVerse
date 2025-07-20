package com.example.app.data

import kotlinx.serialization.Serializable

@Serializable
data class RegisterReq(val name: String, val email: String, val pwd_hash: String)

@Serializable
data class LoginReq(
    val name_or_email: String,
    val pwd_hash: String,
    val maintain_online: Boolean = true
)

@Serializable
data class RefreshTokenReq(val old_token: String)
@Serializable
data class LogoutReq(val old_token: String)
@Serializable
data class ChangePwdReq(
    val name_or_email: String,
    val old_pwd_hash: String,
    val new_pwd_hash: String
)

@Serializable
data class ProfileReq(val token: String)

@Serializable
data class CreateBookReq(val token: String, val book_name: String)
@Serializable
data class ListBooksReq(val token: String)
@Serializable
data class RemoveBookReq(val token: String, val book_id: Int)
@Serializable
data class BookDetailReq(
    val token: String,
    val account_book_id: Int,
    val start_time: String = "",
    val end_time: String = "",
    val note: String = "",
)

@Serializable
data class AddIncomeReq(
    val token: String,
    val account_book_id: Int,
    val amount: Float,
    val income_idx: Int,
    val time: String = "",
    val note: String = "",
)

@Serializable
data class AddOutcomeReq(
    val token: String,
    val account_book_id: Int,
    val amount: Float,
    val outcome_idx: Int,
    val time: String = "",
    val note: String = "",
)
