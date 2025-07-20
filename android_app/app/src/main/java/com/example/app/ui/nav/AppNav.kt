package com.example.app.ui.nav

import androidx.compose.runtime.Composable
import androidx.navigation.compose.*
import com.example.app.ui.screen.*
import com.example.app.ui.nav.Route

@Composable
fun AppNav() {
    val nav = rememberNavController()

    NavHost(nav, startDestination = Route.Splash.pattern) {

        composable(Route.Splash.pattern)   { SplashScreen(nav) }
        composable(Route.Login.pattern)    { LoginScreen(nav)  }
        composable(Route.Register.pattern) { RegisterScreen(nav) }
        composable(Route.Home.pattern)     { HomeScreen(nav)   }

        composable(
            route = Route.Detail.pattern,
            arguments = Route.Detail.args
        ) { backStack ->
            val bookId = backStack.arguments!!.getInt("bookId")
            DetailScreen(nav, bookId)
        }

        composable(
            route = Route.AddIncome.pattern,
            arguments = Route.AddIncome.args
        ) { backStack ->
            val bookId = backStack.arguments!!.getInt("bookId")
            AddIncomeScreen(nav, bookId)
        }

        composable(
            route = Route.AddOutcome.pattern,
            arguments = Route.AddOutcome.args
        ) { backStack ->
            val bookId = backStack.arguments!!.getInt("bookId")
            AddOutcomeScreen(nav, bookId)
        }

        composable(Route.Profile.pattern)  { ProfileScreen(nav) }
    }
}
