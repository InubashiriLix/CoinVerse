/**
 *
 * Please note:
 * This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * Do not edit this file manually.
 *
 */

@file:Suppress(
    "ArrayInDataClass",
    "EnumEntryName",
    "RemoveRedundantQualifierName",
    "UnusedImport"
)

package openapitools.client.models


import kotlinx.serialization.Serializable
import kotlinx.serialization.SerialName
import kotlinx.serialization.Contextual

/**
 * 
 *
 * @param token 
 * @param bookName 
 */
@Serializable

data class CreateAccountBookRequest (

    @SerialName(value = "token")
    val token: kotlin.String,

    @SerialName(value = "book_name")
    val bookName: kotlin.String

) {


}

