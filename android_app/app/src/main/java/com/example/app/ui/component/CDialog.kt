package com.example.app.ui.component

import androidx.compose.material3.*
import androidx.compose.runtime.Composable

@Composable
fun CDialog(show:Boolean,title:String,message:String,onDismiss:()->Unit,onConfirm:()->Unit=onDismiss){
    if(show){
        AlertDialog(onDismissRequest = onDismiss,
            confirmButton={ TextButton(onClick=onConfirm){ Text("OK") } },
            title={ Text(title) }, text={ Text(message) })
    }
}