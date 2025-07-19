package org.openapitools.client.apis

import org.openapitools.client.infrastructure.CollectionFormats.*
import retrofit2.http.*
import retrofit2.Call
import okhttp3.RequestBody
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

import org.openapitools.client.models.AddIncomeRequest
import org.openapitools.client.models.AddIncomeResponse
import org.openapitools.client.models.AddOutcomeRequest
import org.openapitools.client.models.AddOutcomeResponse
import org.openapitools.client.models.BookDetailRequest
import org.openapitools.client.models.BookDetailResponse
import org.openapitools.client.models.ChangePasswordRequest
import org.openapitools.client.models.ChangePasswordResponse
import org.openapitools.client.models.CreateAccountBookRequest
import org.openapitools.client.models.CreateAccountBookResponse
import org.openapitools.client.models.GetUserProfileRequest
import org.openapitools.client.models.GetUserProfileResponse
import org.openapitools.client.models.HTTPValidationError
import org.openapitools.client.models.ListBookRequest
import org.openapitools.client.models.ListBookResponse
import org.openapitools.client.models.LoginRequest
import org.openapitools.client.models.LoginResponse
import org.openapitools.client.models.LogoutRequest
import org.openapitools.client.models.LogoutResponse
import org.openapitools.client.models.RefreshTokenRequest
import org.openapitools.client.models.RefreshTokenResponse
import org.openapitools.client.models.RegisterRequest
import org.openapitools.client.models.RegisterResponse
import org.openapitools.client.models.RemoveBookRequest
import org.openapitools.client.models.RemoveBookResponse

interface InterfacesApi {
    /**
     * POST CoinVerse/book/transactions/add_income
     * add a transaction to the book (need token)
     * 
     * Responses:
     *  - 200: Successful Response
     *  - 422: Validation Error
     *
     * @param addIncomeRequest 
     * @return [Call]<[AddIncomeResponse]>
     */
    @POST("CoinVerse/book/transactions/add_income")
    fun addIncomeCoinVerseBookTransactionsAddIncomePost(@Body addIncomeRequest: AddIncomeRequest): Call<AddIncomeResponse>

    /**
     * POST CoinVerse/book/transactions/add_outcome
     * add a transaction to the book (need token)
     * 
     * Responses:
     *  - 200: Successful Response
     *  - 422: Validation Error
     *
     * @param addOutcomeRequest 
     * @return [Call]<[AddOutcomeResponse]>
     */
    @POST("CoinVerse/book/transactions/add_outcome")
    fun addOutcomeCoinVerseBookTransactionsAddOutcomePost(@Body addOutcomeRequest: AddOutcomeRequest): Call<AddOutcomeResponse>

    /**
     * PUT CoinVerse/users/me/change_password
     * change the user password
     * 
     * Responses:
     *  - 200: Successful Response
     *  - 422: Validation Error
     *
     * @param changePasswordRequest 
     * @return [Call]<[ChangePasswordResponse]>
     */
    @PUT("CoinVerse/users/me/change_password")
    fun changePasswordCoinVerseUsersMeChangePasswordPut(@Body changePasswordRequest: ChangePasswordRequest): Call<ChangePasswordResponse>

    /**
     * POST CoinVerse/create_book
     * create a new account book (need token)
     * 
     * Responses:
     *  - 200: Successful Response
     *  - 422: Validation Error
     *
     * @param createAccountBookRequest 
     * @return [Call]<[CreateAccountBookResponse]>
     */
    @POST("CoinVerse/create_book")
    fun createAccBookCoinVerseCreateBookPost(@Body createAccountBookRequest: CreateAccountBookRequest): Call<CreateAccountBookResponse>

    /**
     * POST CoinVerse/books_detail
     * get the book detail by book_id (need token)
     * 
     * Responses:
     *  - 200: Successful Response
     *  - 422: Validation Error
     *
     * @param bookDetailRequest 
     * @return [Call]<[BookDetailResponse]>
     */
    @POST("CoinVerse/books_detail")
    fun getBookDetailCoinVerseBooksDetailPost(@Body bookDetailRequest: BookDetailRequest): Call<BookDetailResponse>

    /**
     * POST CoinVerse/users/me
     * get the user info
     * 
     * Responses:
     *  - 200: Successful Response
     *  - 422: Validation Error
     *
     * @param getUserProfileRequest 
     * @return [Call]<[GetUserProfileResponse]>
     */
    @POST("CoinVerse/users/me")
    fun getProfileCoinVerseUsersMePost(@Body getUserProfileRequest: GetUserProfileRequest): Call<GetUserProfileResponse>

    /**
     * PUT CoinVerse/list_books
     * list the books in the account (need token)
     * 
     * Responses:
     *  - 200: Successful Response
     *  - 422: Validation Error
     *
     * @param listBookRequest 
     * @return [Call]<[ListBookResponse]>
     */
    @PUT("CoinVerse/list_books")
    fun listAccBookCoinVerseListBooksPut(@Body listBookRequest: ListBookRequest): Call<ListBookResponse>

    /**
     * POST CoinVerse/login
     * name / email + pwd to login, return the token
     * 
     * Responses:
     *  - 200: Successful Response
     *  - 422: Validation Error
     *
     * @param loginRequest 
     * @return [Call]<[LoginResponse]>
     */
    @POST("CoinVerse/login")
    fun loginCoinVerseLoginPost(@Body loginRequest: LoginRequest): Call<LoginResponse>

    /**
     * POST CoinVerse/logout
     * logout, invalidate the token (expire it)
     * 
     * Responses:
     *  - 200: Successful Response
     *  - 422: Validation Error
     *
     * @param logoutRequest 
     * @return [Call]<[LogoutResponse]>
     */
    @POST("CoinVerse/logout")
    fun logoutCoinVerseLogoutPost(@Body logoutRequest: LogoutRequest): Call<LogoutResponse>

    /**
     * POST CoinVerse/refresh_token
     * refresh the token
     * 
     * Responses:
     *  - 200: Successful Response
     *  - 422: Validation Error
     *
     * @param refreshTokenRequest 
     * @return [Call]<[RefreshTokenResponse]>
     */
    @POST("CoinVerse/refresh_token")
    fun refreshTokenCoinVerseRefreshTokenPost(@Body refreshTokenRequest: RefreshTokenRequest): Call<RefreshTokenResponse>

    /**
     * POST CoinVerse/register
     * create new user account
     * 
     * Responses:
     *  - 201: Successful Response
     *  - 422: Validation Error
     *
     * @param registerRequest 
     * @return [Call]<[RegisterResponse]>
     */
    @POST("CoinVerse/register")
    fun registerUserCoinVerseRegisterPost(@Body registerRequest: RegisterRequest): Call<RegisterResponse>

    /**
     * POST CoinVerse/books/remove_book
     * remove the book by book_id (need token)
     * 
     * Responses:
     *  - 200: Successful Response
     *  - 422: Validation Error
     *
     * @param removeBookRequest 
     * @return [Call]<[RemoveBookResponse]>
     */
    @POST("CoinVerse/books/remove_book")
    fun removeBookCoinVerseBooksRemoveBookPost(@Body removeBookRequest: RemoveBookRequest): Call<RemoveBookResponse>

}
