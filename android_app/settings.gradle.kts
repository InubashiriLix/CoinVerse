pluginManagement {
//    plugins {
//        id("org.jetbrains.kotlin.android") version "2.2.1"
//        id("org.jetbrains.kotlin.jvm")     version "2.2.1"
//        id("org.jetbrains.kotlin.plugin.serialization") version "2.2.1"
//    }
    plugins {
        id("com.android.application")            version "8.4.0"          // 你的 AGP
        id("org.jetbrains.kotlin.android")       version "2.2.0"
        id("org.jetbrains.kotlin.jvm")           version "2.2.0"
        id("org.jetbrains.kotlin.plugin.serialization") version "2.2.0"
    }
    repositories { google(); mavenCentral() }
    repositories {
        google {
            content {
                includeGroupByRegex("com\\.android.*")
                includeGroupByRegex("com\\.google.*")
                includeGroupByRegex("androidx.*")
            }
        }
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "app"
include(":app", ":mobile-client")
project(":mobile-client").projectDir = file("mobile-client")
 