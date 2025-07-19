# InterfacesApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
| ------------- | ------------- | ------------- |
| [**addIncomeCoinVerseBookTransactionsAddIncomePost**](InterfacesApi.md#addIncomeCoinVerseBookTransactionsAddIncomePost) | **POST** CoinVerse/book/transactions/add_income | add a transaction to the book (need token) |
| [**addOutcomeCoinVerseBookTransactionsAddOutcomePost**](InterfacesApi.md#addOutcomeCoinVerseBookTransactionsAddOutcomePost) | **POST** CoinVerse/book/transactions/add_outcome | add a transaction to the book (need token) |
| [**changePasswordCoinVerseUsersMeChangePasswordPut**](InterfacesApi.md#changePasswordCoinVerseUsersMeChangePasswordPut) | **PUT** CoinVerse/users/me/change_password | change the user password |
| [**createAccBookCoinVerseCreateBookPost**](InterfacesApi.md#createAccBookCoinVerseCreateBookPost) | **POST** CoinVerse/create_book | create a new account book (need token) |
| [**getBookDetailCoinVerseBooksDetailPost**](InterfacesApi.md#getBookDetailCoinVerseBooksDetailPost) | **POST** CoinVerse/books_detail | get the book detail by book_id (need token) |
| [**getProfileCoinVerseUsersMePost**](InterfacesApi.md#getProfileCoinVerseUsersMePost) | **POST** CoinVerse/users/me | get the user info |
| [**listAccBookCoinVerseListBooksPut**](InterfacesApi.md#listAccBookCoinVerseListBooksPut) | **PUT** CoinVerse/list_books | list the books in the account (need token) |
| [**loginCoinVerseLoginPost**](InterfacesApi.md#loginCoinVerseLoginPost) | **POST** CoinVerse/login | name / email + pwd to login, return the token |
| [**logoutCoinVerseLogoutPost**](InterfacesApi.md#logoutCoinVerseLogoutPost) | **POST** CoinVerse/logout | logout, invalidate the token (expire it) |
| [**refreshTokenCoinVerseRefreshTokenPost**](InterfacesApi.md#refreshTokenCoinVerseRefreshTokenPost) | **POST** CoinVerse/refresh_token | refresh the token |
| [**registerUserCoinVerseRegisterPost**](InterfacesApi.md#registerUserCoinVerseRegisterPost) | **POST** CoinVerse/register | create new user account |
| [**removeBookCoinVerseBooksRemoveBookPost**](InterfacesApi.md#removeBookCoinVerseBooksRemoveBookPost) | **POST** CoinVerse/books/remove_book | remove the book by book_id (need token) |



add a transaction to the book (need token)

### Example
```kotlin
// Import classes:
//import org.openapitools.client.*
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiClient = ApiClient()
val webService = apiClient.createWebservice(InterfacesApi::class.java)
val addIncomeRequest : AddIncomeRequest =  // AddIncomeRequest | 

val result : AddIncomeResponse = webService.addIncomeCoinVerseBookTransactionsAddIncomePost(addIncomeRequest)
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **addIncomeRequest** | [**AddIncomeRequest**](AddIncomeRequest.md)|  | |

### Return type

[**AddIncomeResponse**](AddIncomeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


add a transaction to the book (need token)

### Example
```kotlin
// Import classes:
//import org.openapitools.client.*
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiClient = ApiClient()
val webService = apiClient.createWebservice(InterfacesApi::class.java)
val addOutcomeRequest : AddOutcomeRequest =  // AddOutcomeRequest | 

val result : AddOutcomeResponse = webService.addOutcomeCoinVerseBookTransactionsAddOutcomePost(addOutcomeRequest)
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **addOutcomeRequest** | [**AddOutcomeRequest**](AddOutcomeRequest.md)|  | |

### Return type

[**AddOutcomeResponse**](AddOutcomeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


change the user password

### Example
```kotlin
// Import classes:
//import org.openapitools.client.*
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiClient = ApiClient()
val webService = apiClient.createWebservice(InterfacesApi::class.java)
val changePasswordRequest : ChangePasswordRequest =  // ChangePasswordRequest | 

val result : ChangePasswordResponse = webService.changePasswordCoinVerseUsersMeChangePasswordPut(changePasswordRequest)
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **changePasswordRequest** | [**ChangePasswordRequest**](ChangePasswordRequest.md)|  | |

### Return type

[**ChangePasswordResponse**](ChangePasswordResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


create a new account book (need token)

### Example
```kotlin
// Import classes:
//import org.openapitools.client.*
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiClient = ApiClient()
val webService = apiClient.createWebservice(InterfacesApi::class.java)
val createAccountBookRequest : CreateAccountBookRequest =  // CreateAccountBookRequest | 

val result : CreateAccountBookResponse = webService.createAccBookCoinVerseCreateBookPost(createAccountBookRequest)
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **createAccountBookRequest** | [**CreateAccountBookRequest**](CreateAccountBookRequest.md)|  | |

### Return type

[**CreateAccountBookResponse**](CreateAccountBookResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


get the book detail by book_id (need token)

### Example
```kotlin
// Import classes:
//import org.openapitools.client.*
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiClient = ApiClient()
val webService = apiClient.createWebservice(InterfacesApi::class.java)
val bookDetailRequest : BookDetailRequest =  // BookDetailRequest | 

val result : BookDetailResponse = webService.getBookDetailCoinVerseBooksDetailPost(bookDetailRequest)
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **bookDetailRequest** | [**BookDetailRequest**](BookDetailRequest.md)|  | |

### Return type

[**BookDetailResponse**](BookDetailResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


get the user info

### Example
```kotlin
// Import classes:
//import org.openapitools.client.*
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiClient = ApiClient()
val webService = apiClient.createWebservice(InterfacesApi::class.java)
val getUserProfileRequest : GetUserProfileRequest =  // GetUserProfileRequest | 

val result : GetUserProfileResponse = webService.getProfileCoinVerseUsersMePost(getUserProfileRequest)
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **getUserProfileRequest** | [**GetUserProfileRequest**](GetUserProfileRequest.md)|  | |

### Return type

[**GetUserProfileResponse**](GetUserProfileResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


list the books in the account (need token)

### Example
```kotlin
// Import classes:
//import org.openapitools.client.*
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiClient = ApiClient()
val webService = apiClient.createWebservice(InterfacesApi::class.java)
val listBookRequest : ListBookRequest =  // ListBookRequest | 

val result : ListBookResponse = webService.listAccBookCoinVerseListBooksPut(listBookRequest)
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **listBookRequest** | [**ListBookRequest**](ListBookRequest.md)|  | |

### Return type

[**ListBookResponse**](ListBookResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


name / email + pwd to login, return the token

### Example
```kotlin
// Import classes:
//import org.openapitools.client.*
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiClient = ApiClient()
val webService = apiClient.createWebservice(InterfacesApi::class.java)
val loginRequest : LoginRequest =  // LoginRequest | 

val result : LoginResponse = webService.loginCoinVerseLoginPost(loginRequest)
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **loginRequest** | [**LoginRequest**](LoginRequest.md)|  | |

### Return type

[**LoginResponse**](LoginResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


logout, invalidate the token (expire it)

### Example
```kotlin
// Import classes:
//import org.openapitools.client.*
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiClient = ApiClient()
val webService = apiClient.createWebservice(InterfacesApi::class.java)
val logoutRequest : LogoutRequest =  // LogoutRequest | 

val result : LogoutResponse = webService.logoutCoinVerseLogoutPost(logoutRequest)
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **logoutRequest** | [**LogoutRequest**](LogoutRequest.md)|  | |

### Return type

[**LogoutResponse**](LogoutResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


refresh the token

### Example
```kotlin
// Import classes:
//import org.openapitools.client.*
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiClient = ApiClient()
val webService = apiClient.createWebservice(InterfacesApi::class.java)
val refreshTokenRequest : RefreshTokenRequest =  // RefreshTokenRequest | 

val result : RefreshTokenResponse = webService.refreshTokenCoinVerseRefreshTokenPost(refreshTokenRequest)
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **refreshTokenRequest** | [**RefreshTokenRequest**](RefreshTokenRequest.md)|  | |

### Return type

[**RefreshTokenResponse**](RefreshTokenResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


create new user account

### Example
```kotlin
// Import classes:
//import org.openapitools.client.*
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiClient = ApiClient()
val webService = apiClient.createWebservice(InterfacesApi::class.java)
val registerRequest : RegisterRequest =  // RegisterRequest | 

val result : RegisterResponse = webService.registerUserCoinVerseRegisterPost(registerRequest)
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **registerRequest** | [**RegisterRequest**](RegisterRequest.md)|  | |

### Return type

[**RegisterResponse**](RegisterResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


remove the book by book_id (need token)

### Example
```kotlin
// Import classes:
//import org.openapitools.client.*
//import org.openapitools.client.infrastructure.*
//import org.openapitools.client.models.*

val apiClient = ApiClient()
val webService = apiClient.createWebservice(InterfacesApi::class.java)
val removeBookRequest : RemoveBookRequest =  // RemoveBookRequest | 

val result : RemoveBookResponse = webService.removeBookCoinVerseBooksRemoveBookPost(removeBookRequest)
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **removeBookRequest** | [**RemoveBookRequest**](RemoveBookRequest.md)|  | |

### Return type

[**RemoveBookResponse**](RemoveBookResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

