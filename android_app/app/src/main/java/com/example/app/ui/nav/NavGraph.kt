package com.example.app.ui.nav

import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.NavHostController
import androidx.navigation.compose.composable
import androidx.navigation.NavType
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.example.app.ui.screen.*

@Composable
fun AppNavGraph(startDest: String = Route.Splash.path, navController: NavHostController = rememberNavController()) {
    NavHost(navController, startDest) {
        composable(Route.Splash.path) { SplashScreen(navController) }
        composable(Route.Login.path)  { LoginScreen(navController) }
        composable(Route.Register.path){ RegisterScreen(navController) }
        composable(Route.Home.path)   { HomeScreen(navController) }
        composable(Route.Profile.path){ ProfileScreen(navController) }
        composable(
            Route.Detail.path,
            arguments = listOf(navArgument("bookId"){type= NavType.IntType})) {
            DetailScreen(navController, it.arguments!!.getInt("bookId"))
        }
        composable(
            Route.AddIncome.path,
            arguments = listOf(navArgument("bookId"){type= NavType.IntType})) {
            AddIncomeSheet(navController, it.arguments!!.getInt("bookId"))
        }
        composable(
            Route.AddOutcome.path,
            arguments = listOf(navArgument("bookId"){type= NavType.IntType})) {
            AddOutcomeSheet(navController, it.arguments!!.getInt("bookId"))
        }
    }
}