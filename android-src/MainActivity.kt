package com.karnea.coachcalli

import android.os.Bundle
import com.getcapacitor.BridgeActivity

class MainActivity : BridgeActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        // Enregistre le pont natif du minuteur AVANT le chargement du web.
        registerPlugin(CoachCalliTimerPlugin::class.java)
        super.onCreate(savedInstanceState)
    }
}
