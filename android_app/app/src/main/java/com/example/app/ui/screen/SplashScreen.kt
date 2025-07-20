package com.example.app.ui.screen

import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.navigation.NavHostController
import com.example.app.ui.nav.Route
import com.example.app.vm.SplashVM
import androidx.compose.foundation.layout.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel

@Composable
fun SplashScreen(nav: NavHostController, vm: SplashVM = viewModel()){
    val state by vm.state.collectAsState()
    when(state){
        is com.example.app.vm.SplashState.Loading -> Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center){ CircularProgressIndicator() }
        com.example.app.vm.SplashState.ToAuth -> nav.navigate(Route.Login.path){ popUpTo(Route.Splash.path){inclusive=true} }
        com.example.app.vm.SplashState.ToHome -> nav.navigate(Route.Home.path){ popUpTo(Route.Splash.path){inclusive=true} }
    }
}