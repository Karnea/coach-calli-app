#!/usr/bin/env python3
"""Insère la config de signature debug (notre keystore) dans app/build.gradle.
Appelé par le workflow GitHub Actions. Idempotent."""
import sys, re

path = sys.argv[1] if len(sys.argv) > 1 else "android/app/build.gradle"
s = open(path).read()

if "coach-calli.keystore" in s:
    print("signingConfig déjà présent, rien à faire")
    sys.exit(0)

sign = """    signingConfigs {
        debug {
            storeFile file('coach-calli.keystore')
            storePassword 'coachcalli2026'
            keyAlias 'coachcalli'
            keyPassword 'coachcalli2026'
        }
    }
"""

s = re.sub(r'(android\s*\{\s*\n)', r'\1' + sign, s, count=1)

if "buildTypes {" in s and "debug {\n            signingConfig" not in s:
    s = s.replace(
        "buildTypes {\n",
        "buildTypes {\n        debug {\n            signingConfig signingConfigs.debug\n        }\n",
        1,
    )

open(path, "w").write(s)
print("signingConfig debug inséré")
