plugins {
    kotlin("jvm") version "2.2.1"
    kotlin("plugin.serialization") version "2.2.1"
}

kotlin {
    compilerOptions {
        // ↓ ↓ ↓ 仅这一行即可把 K2 关闭，IDE 的 “deprecated” 警告也没了
        languageVersion.set(org.jetbrains.kotlin.gradle.dsl.KotlinVersion.KOTLIN_1_9)
        /* 你也可以写成字符串：
           languageVersion.set("1.9")
        */
    }
}

repositories {
    google()
    mavenCentral()
}

dependencies {
    implementation(platform("org.jetbrains.kotlin:kotlin-bom:2.2.0"))
    val retrofitBom = platform("com.squareup.retrofit2:retrofit-bom:2.11.0")
    implementation(retrofitBom)
    implementation(platform("com.squareup.retrofit2:retrofit-bom:2.11.0"))
    implementation("com.squareup.retrofit2:retrofit")
    implementation("com.squareup.retrofit2:converter-kotlinx-serialization")
    implementation("com.squareup.retrofit2:retrofit")
    implementation("com.squareup.retrofit2:converter-kotlinx-serialization")
    implementation("com.squareup.retrofit2:converter-scalars")
    implementation("com.squareup.okhttp3:okhttp:5.2.1")
    implementation("com.squareup.okhttp3:logging-interceptor:5.2.1")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.9.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.10.2")
}
