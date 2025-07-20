package com.example.app.ui.screen

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import com.example.app.ui.nav.Route
import com.example.app.vm.HomeVM
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.app.ui.component.CDialog
import com.example.app.ui.theme.CVTheme
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.ui.Alignment
import com.example.app.ui.theme.AppTheme
import com.example.app.data.TokenStore
import com.example.app.data.*
import androidx.compose.foundation.lazy.items

@Composable
fun HomeScreen(nav: NavHostController, vm: HomeVM = viewModel()) {

    val ui by vm.state      // <- 收集 State

    // 首次进入加载
    LaunchedEffect(Unit) {
        val token = TokenStore.getToken() ?: ""
        vm.load(token)
    }

    AppTheme {
        Scaffold(
            topBar = { CenterAlignedTopAppBar(title = { Text("账本") }) },
            floatingActionButton = { /* 省略 */ }
        ) { pad ->

            // loading 指示
            if (ui.isLoading) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else {
                LazyColumn(contentPadding = pad) {
                    items(ui.books) { book ->
                        /* …点击跳转… */
                    }
                }
            }
        }

        CDialog(
            show = ui.errorMsg != null,
            title = "错误",
            message = ui.errorMsg ?: "",
            onDismiss = vm::dismissError
        )
    }
}