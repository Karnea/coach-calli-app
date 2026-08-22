package com.karnea.coachcalli

import android.content.ActivityNotFoundException
import android.content.Intent
import android.provider.AlarmClock
import com.getcapacitor.Plugin
import com.getcapacitor.PluginCall
import com.getcapacitor.PluginMethod
import com.getcapacitor.annotation.CapacitorPlugin

@CapacitorPlugin(name = "CoachCalliTimer")
class CoachCalliTimerPlugin : Plugin() {

    @PluginMethod
    fun start(call: PluginCall) {
        val seconds = call.getInt("seconds") ?: 0
        val message = call.getString("message") ?: "Repos Coach Calli"

        if (seconds <= 0) {
            call.reject("Duree invalide")
            return
        }

        // 1) Tentative directe : minuteur SET_TIMER (implicite, sans package).
        val timerIntent = Intent(AlarmClock.ACTION_SET_TIMER).apply {
            putExtra(AlarmClock.EXTRA_LENGTH, seconds)
            putExtra(AlarmClock.EXTRA_MESSAGE, message)
            putExtra(AlarmClock.EXTRA_SKIP_UI, false)
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
        }
        try {
            context.startActivity(timerIntent)
            call.resolve()
            return
        } catch (e: ActivityNotFoundException) {
            // On continue vers le repli ci-dessous.
        } catch (e: Exception) {
            call.reject("Erreur au lancement du minuteur : " + e.message)
            return
        }

        // 2) Repli : ouvrir simplement l'app Horloge Google (sans pre-remplir).
        try {
            val launch = context.packageManager
                .getLaunchIntentForPackage("com.google.android.deskclock")
            if (launch != null) {
                launch.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                context.startActivity(launch)
                call.resolve()
                return
            }
        } catch (e: Exception) {
            // ignore
        }

        call.reject("Impossible d'ouvrir l'application Horloge")
    }
}
