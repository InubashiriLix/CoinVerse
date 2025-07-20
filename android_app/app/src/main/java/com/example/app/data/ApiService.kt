package com.example.app.data

import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.http.PUT

interface ApiService {
    @POST("/CoinVerse/register")
    suspend fun register(@Body req: RegisterReq): ApiEnvelope<Unit>

    @POST("/CoinVerse/login")
    suspend fun login(@Body req: LoginReq): ApiEnvelope<Unit>

    @POST("/CoinVerse/refresh_token")
    suspend fun refreshToken(@Body req: RefreshTokenReq): ApiEnvelope<Unit>

    @POST("/CoinVerse/logout")
    suspend fun logout(@Body req: LogoutReq): ApiEnvelope<Unit>

    @PUT("/CoinVerse/users/me/change_password")
    suspend fun changePassword(@Body req: ChangePwdReq): ApiEnvelope<Unit>

    @POST("/CoinVerse/users/me")
    suspend fun profile(@Body req: ProfileReq): ApiEnvelope<Unit>

    @POST("/CoinVerse/create_book")
    suspend fun createBook(@Body req: CreateBookReq): ApiEnvelope<Unit>

    @PUT("/CoinVerse/list_books")
    suspend fun listBooks(@Body req: ListBooksReq): ApiEnvelope<Unit>

    @POST("/CoinVerse/books/remove_book")
    suspend fun removeBook(@Body req: RemoveBookReq): ApiEnvelope<Unit>

    @POST("/CoinVerse/books_detail")
    suspend fun bookDetail(@Body req: BookDetailReq): ApiEnvelope<Unit>

    @POST("/CoinVerse/book/transactions/add_income")
    suspend fun addIncome(@Body req: AddIncomeReq): ApiEnvelope<Unit>

    @POST("/CoinVerse/book/transactions/add_outcome")
    suspend fun addOutcome(@Body req: AddOutcomeReq): ApiEnvelope<Unit>
}
