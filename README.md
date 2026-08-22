# Coach Calli — application Android

Cette version transforme ton app web Coach Calli en **vraie application Android**.
Le bouton « Minuteur Horloge » lance désormais l'app Horloge de ton téléphone
sans passer par Chrome — donc sans le blocage qu'on avait.

Tu n'as **pas besoin d'installer quoi que ce soit** sur ton ordinateur.
GitHub compile l'application pour toi et te donne un fichier `.apk` à installer.

---

## Comment obtenir l'APK (une seule fois à comprendre, ~5 min)

### 1. Mettre ces fichiers sur GitHub
- Crée un nouveau dépôt sur GitHub (par exemple `coach-calli-app`).
- Envoie-y **tout le contenu de ce dossier** (glisser-déposer via le bouton
  « Add file » → « Upload files » sur le site GitHub suffit).

### 2. Lancer la compilation
- Va dans l'onglet **Actions** de ton dépôt.
- Si GitHub demande d'activer les workflows, clique pour confirmer.
- La compilation démarre toute seule dès l'envoi des fichiers.
  Sinon, clique sur « Build Coach Calli APK » puis « Run workflow ».

### 3. Récupérer le fichier
- Attends ~3 à 5 minutes (rond orange → coche verte).
- Clique sur la ligne du build terminé.
- En bas, section **Artifacts**, télécharge **coach-calli-apk**.
- Dézippe-le : tu obtiens `coach-calli.apk`.

### 4. Installer sur le Pixel
- Envoie-toi le fichier `.apk` (Drive, mail, câble…).
- Ouvre-le sur le téléphone.
- Android demandera d'autoriser « installer des applications inconnues »
  pour l'app qui ouvre le fichier (Fichiers ou Chrome) : accepte.
- L'app **Coach Calli** s'installe comme une vraie application.

---

## Pourquoi ça marche maintenant

Avant, l'app était une page web dans Chrome, et Chrome **interdit** à une page
web de lancer l'Horloge (mesure de sécurité). Là, c'est une **application native** :
elle a le droit de lancer l'Horloge, exactement comme n'importe quelle app.

Le bouton appelle un petit morceau de code natif (`CoachCalliTimerPlugin.kt`)
qui déclenche le minuteur de l'Horloge à la bonne durée.

---

## Tes données sont conservées

L'app garde Firebase : tu te reconnectes avec Google et tu retrouves tout ton
historique de séances. Rien n'est perdu.

---

## Si la compilation échoue

Ouvre le build rouge dans l'onglet Actions, regarde quelle étape a échoué,
et envoie-moi le message d'erreur : je corrige.
