package com.example.app.ui.screen

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import com.example.app.ui.nav.Route
import androidx.compose.ui.text.input.PasswordVisualTransformation
import com.example.app.ui.theme.CVTheme
import com.example.app.vm.AuthVM
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.app.ui.component.CDialog
import com.example.app.data.ServerStore
import com.example.app.ui.theme.AppTheme
import kotlinx.coroutines.launch

@Composable
fun LoginScreen(
    nav: NavHostController,
    vm: AuthVM = viewModel()
) {
    var server by remember { mutableStateOf("") }
    var email  by remember { mutableStateOf("") }
    var pwd    by remember { mutableStateOf("") }

    /* 首次进入读服务器地址 */
    LaunchedEffect(Unit) {
        server = ServerStore.get() ?: "http://192.168.31.135:1919"
    }

    /* 用 Compose scope 启协程 */
    val scope = rememberCoroutineScope()

    AppTheme {
        Scaffold(topBar = { CenterAlignedTopAppBar(title = { Text("登录") }) }) { pad ->
            Column(
                Modifier.padding(pad).padding(24.dp).fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                OutlinedTextField(
                    value = server,
                    onValueChange = { server = it },
                    label = { Text("服务器地址") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = email,
                    onValueChange = { email = it },
                    label = { Text("Email / Name") },
                    modifier = Modifier.fillMaxWidth()
                )
                OutlinedTextField(
                    value = pwd,
                    onValueChange = { pwd = it },
                    label = { Text("Password") },
                    visualTransformation = PasswordVisualTransformation(),
                    modifier = Modifier.fillMaxWidth()
                )

                Button(
                    onClick = {
                        scope.launch {
                            vm.loginWithServer(server, email, pwd) {
                                nav.navigate(Route.Home.path) {
                                    popUpTo(0) { inclusive = true }
                                }
                            }
                        }
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    if (vm.loading.value) {
                        CircularProgressIndicator(strokeWidth = 2.dp, modifier = Modifier.size(20.dp))
                    } else Text("登录")
                }

                TextButton(onClick = { nav.navigate(Route.Register.path) }) {
                    Text("没有账号？注册")
                }
            }
        }

        CDialog(
            show = vm.error.value != null,
            title = "错误",
            message = vm.error.value ?: "",
            onDismiss = { vm.error.value = null }
        )
    }
}