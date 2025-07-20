// Top-level build file where you can add configuration options common to all sub-projects/modules.
plugins {
    alias(libs.plugins.android.application) apply false
    alias(libs.plugins.kotlin.android) apply false
    alias(libs.plugins.kotlin.compose) apply false
}

//dependencies {
//    implementation(platform("androidx.compose:compose-bom:2024.04.00"))
//
//    // retrofit & Kotlinx‑serialization
//    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.9.0")
//    implementation("com.squareup.retrofit2:converter-kotlinx-serialization")
//
//}