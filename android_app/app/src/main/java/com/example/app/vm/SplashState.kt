package com.example.app.vm

sealed interface SplashState {
    object Loading : SplashState
    object ToAuth  : SplashState
    object ToHome  : SplashState
}