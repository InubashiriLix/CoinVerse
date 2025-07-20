package com.example.app.ui.nav

import androidx.navigation.NavType
import androidx.navigation.navArgument

sealed class Route(
    /** 用于 NavHost 的 route pattern（可含占位符） */
    val pattern: String
) {
    /** 兼容旧代码的别名，让 .path 和 .pattern 都能用 */
    val path: String
        get() = pattern

    object Splash    : Route("splash")
    object Login     : Route("auth/login")
    object Register  : Route("auth/register")
    object Home      : Route("main/home")

    object Detail    : Route("main/detail/{bookId}") {
        fun build(bookId: Int) = "main/detail/$bookId"
        val args = listOf(navArgument("bookId") { type = NavType.IntType })
    }

    object AddIncome : Route("main/add_income/{bookId}") {
        fun build(bookId: Int) = "main/add_income/$bookId"
        val args = listOf(navArgument("bookId") { type = NavType.IntType })
    }

    object AddOutcome : Route("main/add_outcome/{bookId}") {
        fun build(bookId: Int) = "main/add_outcome/$bookId"
        val args = listOf(navArgument("bookId") { type = NavType.IntType })
    }

    object Profile   : Route("profile")
}
