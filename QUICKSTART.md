# Quick Start Guide - v2.0

## Schnelleinstieg in 5 Schritten

### 1️⃣ Voraussetzungen prüfen

```bash
# Python-Version prüfen (3.7+ erforderlich)
python3 --version

# PlatformIO prüfen
pio --version

# Optional: PyYAML für YAML-Konfiguration
pip install pyyaml
```

Falls PlatformIO fehlt:
```bash
pip install platformio
```

### 2️⃣ Konfiguration anpassen

#### Copyright-Header bearbeiten

```bash
cd /Users/andy/PlatformIO/GITLAB/code-obfuscator
nano copyright_header.txt
```

Ersetze:
- `[Dein Firmenname / Dein Name]` → Dein Name/Firma
- `[deine-email@example.com]` → Deine E-Mail
- `[www.example.com]` → Deine Website

#### Konfigurationsdatei prüfen

```bash
nano config.yaml
```

Wichtigste Einstellungen:
```yaml
# Welche Ordner sollen obfusciert werden?
obfuscate_folders:
  - "src"
  - "lib/Kaninchen"
  - "include"

# Welche Libraries sollen NICHT obfusciert werden?
preserve_libraries:
  - "lib/ArduinoJson"
  - "lib/WiFi"
  # ... alle externen Libraries

# Nur verwendete Libraries kopieren?
copy_only_used_libraries: true
```

### 3️⃣ Tool ausführen

```bash
cd /Users/andy/PlatformIO/GITLAB/code-obfuscator

# Standard-Ausführung
python3 obfuscate_project.py \
    /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-main \
    /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated
```

### 4️⃣ Ergebnis prüfen

```bash
# Prüfe Copyright-Header in Kaninchen-Dateien
head -35 /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated/lib/Kaninchen/src/main.cpp

# Prüfe ob externe Libraries unverändert sind
cat /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated/lib/ArduinoJson/src/ArduinoJson.h

# Prüfe die Mapping-Datei
cat /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated/obfuscation_mapping.json

# Optional: Manuell kompilieren
cd /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated
pio run
```

### 5️⃣ Projektgröße vergleichen

```bash
# Original-Projekt
du -sh /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-main

# Obfusciertes Projekt (sollte kleiner sein durch Library-Filtering)
du -sh /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated
```

---

## 🆕 Was ist neu in v2.0?

### Copyright-Header
✅ Alle `lib/Kaninchen` Dateien erhalten automatisch einen Copyright-Header

### Selektive Library-Verarbeitung
✅ Nur verwendete Libraries werden kopiert  
✅ Externe Libraries bleiben UNVERÄNDERT (Kommentare, Namen bleiben)  
✅ Beispiele, Tests, Dokumentation werden automatisch entfernt  

### Ergebnis
- ✅ Kleineres Projekt (50-80% weniger Library-Dateien)
- ✅ Lesbare externe Libraries (einfacher zu debuggen)
- ✅ Geschützter eigener Code (lib/Kaninchen)

---

## Optionen

### Mit ausführlicher Ausgabe
```bash
python3 obfuscate_project.py source target --verbose
```

Zeigt:
- Welche Libraries werden verwendet
- Welche Dateien werden kopiert/ignoriert
- Welche Identifikatoren werden umbenannt
- Copyright-Header-Status

### Ohne Kompilierung (schneller)
```bash
python3 obfuscate_project.py source target --skip-compile
```

Nützlich für:
- Schnelles Testen der Konfiguration
- Iteratives Anpassen der Einstellungen

### Mit eigener Konfiguration
```bash
python3 obfuscate_project.py source target --config my_config.yaml
```

---

## Beispiel-Output

```
============================================================
PlatformIO PROJECT OBFUSCATOR
============================================================
Source: /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-main
Target: /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated
============================================================

[INFO] Projekt kopiert: /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated

[INFO] Obfuscation-Mapping gespeichert: obfuscation_mapping.json
[INFO] Anzahl obfuscierter Identifikatoren: 247

============================================================
KOMPILIERUNG
============================================================

[INFO] Kompiliere Projekt in /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated...
[INFO] Dies kann einige Minuten dauern...

[ERFOLG] ✓ Kompilierung erfolgreich!

============================================================
ZUSAMMENFASSUNG
============================================================
Verarbeitete Dateien: 42
Obfuscierte Identifikatoren: 247
Kompilierung: ✓ ERFOLGREICH
Obfusciertes Projekt: /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated
============================================================
```

---

## Problemlösung

### Problem: "platformio.ini fehlt"
→ Stelle sicher, dass der Source-Pfad ein gültiges PlatformIO-Projekt ist

### Problem: "Kompilierung fehlgeschlagen"
→ Führe mit `--skip-compile` aus und kompiliere manuell:
```bash
cd target_folder
pio run
```
→ Prüfe die Compiler-Fehler und passe ggf. `RESERVED_WORDS` im Script an

### Problem: "Target existiert bereits"
→ Das Tool fragt nach Bestätigung zum Überschreiben
→ Oder lösche den Zielordner vorher manuell: `rm -rf target_folder`

---

## Weitere Hilfe

Detaillierte Dokumentation: Siehe [README.md](README.md)

Hilfe anzeigen:
```bash
python3 obfuscate_project.py --help
```

---

**Viel Erfolg! 🚀**
