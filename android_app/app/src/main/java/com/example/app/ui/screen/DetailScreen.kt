package com.example.app.ui.screen

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Remove
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.navigation.NavHostController
import com.example.app.ui.theme.AppTheme
import com.example.app.ui.nav.Route

@Composable
fun DetailScreen(nav: NavHostController, bookId: Int) {
    AppTheme {
        Scaffold(
            topBar = {
                CenterAlignedTopAppBar(
                    title = { Text("账本 #$bookId") },
                    navigationIcon = {
                        IconButton(onClick = { nav.popBackStack() }) {
                            Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                        }
                    }
                )
            },
            floatingActionButton = {
                Column {
                    FloatingActionButton(
                        onClick = { nav.navigate(Route.AddIncome.build(bookId)) }
                    ) { Icon(Icons.Default.Add, contentDescription = "Add Income") }

                    Spacer(Modifier.height(16.dp))

                    FloatingActionButton(
                        onClick = { nav.navigate(Route.AddOutcome.build(bookId)) }
                    ) { Icon(Icons.Default.Remove, contentDescription = "Add Outcome") }
                }
            }
        ) { pad ->
            /* TODO: LazyColumn of transactions */
            Box(Modifier.padding(pad))
        }
    }
}
