package com.karnea.coachcalli

import android.content.Intent
import android.provider.AlarmClock
import com.getcapacitor.Plugin
import com.getcapacitor.PluginCall
import com.getcapacitor.PluginMethod
import com.getcapacitor.annotation.CapacitorPlugin

/**
 * Pont natif : expose CoachCalliTimer au JavaScript de l'app web.
 * Depuis du code natif, lancer l'Horloge est un simple appel système,
 * sans les restrictions que Chrome impose à une PWA.
 */
@CapacitorPlugin(name = "CoachCalliTimer")
class CoachCalliTimerPlugin : Plugin() {

    @PluginMethod
    fun start(call: PluginCall) {
        val seconds = call.getInt("seconds") ?: 0
        val message = call.getString("message") ?: "Repos Coach Calli"

        if (seconds <= 0) {
            call.reject("Durée invalide")
            return
        }

        try {
            val intent = Intent(AlarmClock.ACTION_SET_TIMER).apply {
                putExtra(AlarmClock.EXTRA_LENGTH, seconds)
                putExtra(AlarmClock.EXTRA_MESSAGE, message)
                // false = on affiche l'app Horloge (chrono visible + sonnerie).
                putExtra(AlarmClock.EXTRA_SKIP_UI, false)
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            }

            // Vérifie qu'une app peut gérer l'intent avant de lancer.
            if (intent.resolveActivity(context.packageManager) != null) {
                context.startActivity(intent)
                call.resolve()
            } else {
                // Aucune horloge ne gère SET_TIMER : on tente l'ouverture simple.
                val fallback = context.packageManager
                    .getLaunchIntentForPackage("com.google.android.deskclock")
                if (fallback != null) {
                    fallback.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                    context.startActivity(fallback)
                    call.resolve()
                } else {
                    call.reject("Aucune application Horloge trouvée")
                }
            }
        } catch (e: Exception) {
            call.reject("Impossible de lancer le minuteur : " + e.message)
        }
    }
}
