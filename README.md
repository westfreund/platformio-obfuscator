# PlatformIO Project Obfuscator v2.0

Ein erweitertes Python-Tool zur automatischen Code-Obfuscation von PlatformIO-Projekten. Das Tool entfernt selektiv Kommentare, ersetzt Variablen- und Funktionsnamen durch generische Bezeichnungen, fügt Copyright-Header hinzu und kopiert nur verwendete Libraries, während die Funktionalität des Codes erhalten bleibt.

## 📋 Inhaltsverzeichnis

- [Überblick](#überblick)
- [Was ist neu in v2.0](#was-ist-neu-in-v20)
- [Features](#features)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Schnelleinstieg](#schnelleinstieg)
- [Verwendung](#verwendung)
- [Konfiguration](#konfiguration)
- [Funktionsweise](#funktionsweise)
- [Beispiele](#beispiele)
- [Wichtige Hinweise](#wichtige-hinweise)
- [Troubleshooting](#troubleshooting)
- [Technische Details](#technische-details)

---

## 🎯 Überblick

Dieses Tool wurde entwickelt, um PlatformIO-Projekte für die Veröffentlichung vorzubereiten, indem es:

1. **Copyright-Header hinzufügt**: Konfigurierbare Copyright-Header für definierte Ordner (z.B. `src`, `lib/Askoheat`, `include`)
2. **Selektiv obfusciert**: Nur definierte Ordner (`src`, `lib/Askoheat`, `include`) werden obfusciert
3. **Flexible Verschleierung**: 4 verschiedene Verschleierungsstile - von einfach bis hochgradig obfusciert
4. **Libraries schützt**: Externe Libraries bleiben lesbar - nur eigener Code wird obfusciert
5. **Intelligent kopiert**: Nur verwendete Libraries werden kopiert, Beispiele werden entfernt
6. **Kommentare entfernt**: Alle `//` und `/* */` Kommentare werden aus obfuscierten Ordnern entfernt
7. **Code obfusciert**: Variablen, Funktionen und andere Identifikatoren werden durch generische Namen ersetzt
8. **Projekt kopiert**: Das Originalprojekt bleibt unverändert, es wird eine neue Kopie erstellt
9. **Kompilierung prüft**: Das obfuscierte Projekt wird automatisch kompiliert, um die Funktionalität zu verifizieren

---

## 🆕 Was ist neu in v2.0?

### Hauptfeatures

#### ✨ Copyright-Header-System
- Automatisches Hinzufügen von Copyright-Headern zu konfigurierbaren Ordnern
- Standard: `src`, `lib/Askoheat`, `include` (vollständig anpassbar)
- Vollständig anpassbar über `copyright_header.txt`
- Unterstützt alle gängigen Lizenz-Stile (MIT, GPL, proprietär, etc.)

#### ✨ Selektive Library-Verarbeitung
- **Dependency-Analyse**: Erkennt automatisch, welche Libraries tatsächlich verwendet werden
- **Preservation-Mode**: Externe Libraries werden NICHT obfusciert - Kommentare und Namen bleiben erhalten
- **Intelligentes Filtering**: Beispiele, Tests, Dokumentation werden automatisch aus Libraries entfernt
- **Projektgrößen-Optimierung**: Reduziert Projektgröße erheblich durch Entfernen ungenutzter Dateien

#### ✨ YAML-Konfigurationssystem
- Umfassende `config.yaml` für alle Einstellungen
- Definiere selbst, welche Ordner obfusciert werden sollen
- Konfigurierbare Copyright-Ordner (nicht mehr hardcoded auf `lib/Askoheat`)
- Konfigurierbare Library-Behandlung
- **4 Verschleierungsstile**: `simple`, `random`, `hex`, `numbered`
  - `simple`: v0, v1, C0, C1 (schnell lesbar)
  - `random`: z8K3a, mP9xQ (hochgradig obfusciert)
  - `hex`: x4F2A, x7B3C (Hex-basiert)
  - `numbered`: var_0, var_1, const_0 (beschreibend)
- Anpassbare Identifier-Länge (bei random/hex)

### Detaillierte Änderungen

Siehe [CHANGELOG.md](CHANGELOG.md) für vollständige Liste.

---

## ✨ Features

### v2.1 Features (NEU!)
- ✅ **Konfigurierbare Copyright-Ordner**: Copyright-Header nicht mehr auf `lib/Askoheat` beschränkt
- ✅ **Mehrere Verschleierungsstile**: 4 verschiedene Obfuscation-Modi (simple, random, hex, numbered)
- ✅ **Erweiterte src-Unterstützung**: src-Ordner kann nun auch Copyright-Header erhalten
- ✅ **Anpassbare Obfuscation-Tiefe**: Definiere Verschleierungsintensität nach Bedarf

### v2.0 Features
- ✅ **Copyright-Header-System**: Automatisches Hinzufügen von Copyright-Headern
- ✅ **Selektive Obfuscation**: Nur definierte Ordner werden obfusciert, Libraries bleiben lesbar
- ✅ **Dependency-Analyse**: Automatische Erkennung verwendeter Libraries
- ✅ **Library-Filtering**: Entfernt Beispiele, Tests, Dokumentation aus Libraries
- ✅ **YAML-Konfiguration**: Zentrale Konfigurationsdatei für alle Einstellungen
- ✅ **Preservation-Mode**: Externe Libraries bleiben unverändert und wartbar

### Bewährte Features (v1.0)
- ✅ **Vollständige Projektkopie**: Sicheres Arbeiten ohne das Original zu verändern
- ✅ **Kommentar-Entfernung**: Entfernt einzeilige (`//`) und mehrzeilige (`/* */`) Kommentare
- ✅ **Intelligente Obfuscation**: Ersetzt nur benutzerdefinierte Identifikatoren
- ✅ **Schutz von Keywords**: C/C++ Keywords und Standardfunktionen bleiben unverändert
- ✅ **Arduino/ESP32 Support**: Erkennt und schützt Arduino/ESP32 Standardfunktionen
- ✅ **Mapping-Datei**: Speichert die Zuordnung Original → Obfusciert für Debugging
- ✅ **Automatische Kompilierung**: Verifiziert das obfuscierte Projekt mit PlatformIO
- ✅ **Verbose-Modus**: Detaillierte Ausgabe für Debugging
- ✅ **Fehlerbehandlung**: Robuste Fehlerbehandlung und aussagekräftige Fehlermeldungen

---

## 📦 Voraussetzungen

### Software

- **Python 3.7+** (empfohlen: Python 3.8 oder höher)
- **PlatformIO Core** (für die Kompilierung)
- **PyYAML** (optional, für YAML-Konfiguration)
- **Betriebssystem**: macOS, Linux, Windows

### Python-Module

#### Erforderlich (Standard-Library):
- `os`, `sys`, `re`, `shutil`, `subprocess`, `argparse`, `json`, `pathlib`, `typing`, `hashlib`, `fnmatch`

Keine zusätzlichen pip-Installationen erforderlich! ✨

#### Optional:
- **PyYAML**: Für YAML-Konfiguration (empfohlen)
  ```bash
  pip install pyyaml
  ```
  
  Falls PyYAML nicht installiert ist, kann auch JSON verwendet werden.

### PlatformIO Installation

Falls PlatformIO noch nicht installiert ist:

```bash
# macOS/Linux
pip install platformio

# Oder mit Homebrew (macOS)
brew install platformio

# Oder direkt von der Website
curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py -o get-platformio.py
python3 get-platformio.py
```

Prüfe die Installation:
```bash
pio --version
```

---

## 🚀 Installation

1. **Tool herunterladen**: Das Projekt in einen eigenen Ordner platzieren

```bash
cd /path/to/your/directory
mkdir code-obfuscator
cd code-obfuscator
# obfuscate_project.py hierher kopieren
```

2. **Ausführbar machen** (optional, Unix/macOS/Linux):

```bash
chmod +x obfuscate_project.py
```

3. **Optional: PyYAML installieren**:

```bash
pip install pyyaml
```

4. **Konfiguration anpassen**:

```bash
# Copyright-Header anpassen
nano copyright_header.txt

# Konfiguration anpassen
nano config.yaml
```

5. **Fertig!** Das Tool ist einsatzbereit.

---

## 🚀 Schnelleinstieg

### Schritt 1: Copyright-Header anpassen

Bearbeite `copyright_header.txt`:
```bash
nano copyright_header.txt
```

Ersetze:
- `[Dein Firmenname / Dein Name]` → Dein Name
- `[deine-email@example.com]` → Deine E-Mail
- `[www.example.com]` → Deine Website

### Schritt 2: Konfiguration prüfen

Bearbeite `config.yaml`:
```bash
nano config.yaml
```

Wichtigste Einstellungen:
- `obfuscate_folders`: Welche Ordner sollen obfusciert werden?
- `preserve_libraries`: Welche Libraries sollen NICHT obfusciert werden?
- `copy_only_used_libraries`: Nur verwendete Libraries kopieren?

### Schritt 3: Tool ausführen

```bash
python3 obfuscate_project.py \
    /path/to/source/project \
    /path/to/target/project
```

### Schritt 4: Ergebnis prüfen

```bash
# Prüfe Copyright-Header
head -30 /path/to/target/project/lib/Askoheat/src/main.cpp

# Prüfe Mapping
cat /path/to/target/project/obfuscation_mapping.json

# Prüfe Kompilierung
cd /path/to/target/project
pio run
```

---

## 💻 Verwendung

### Grundlegende Syntax

```bash
python3 obfuscate_project.py <source> <target> [optionen]
```

### Parameter

| Parameter | Beschreibung | Erforderlich | Neu in v2.0 |
|-----------|--------------|--------------|-------------|
| `source` | Pfad zum Quell-PlatformIO-Projekt | ✅ Ja | |
| `target` | Pfad für das obfuscierte Projekt | ✅ Ja | |
| `-c, --config` | Pfad zur Konfigurationsdatei (YAML/JSON) | ❌ Nein | ✅ |
| `-v, --verbose` | Ausführliche Ausgabe | ❌ Nein | |
| `-s, --skip-compile` | Kompilierung überspringen | ❌ Nein | |
| `-h, --help` | Hilfe anzeigen | ❌ Nein | |

### Beispiel-Aufrufe

**Standard-Verwendung mit automatischer Config:**
```bash
python3 obfuscate_project.py \
    /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-main \
    /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated
```

**Mit spezifischer Konfiguration:**
```bash
python3 obfuscate_project.py \
    /path/to/source \
    /path/to/target \
    --config my_config.yaml
```

**Mit ausführlicher Ausgabe:**
```bash
python3 obfuscate_project.py \
    /path/to/source \
    /path/to/target \
    --verbose
```

**Ohne Kompilierung (schneller für Tests):**
```bash
python3 obfuscate_project.py \
    /path/to/source \
    /path/to/target \
    --skip-compile
```

**Kombination:**
```bash
python3 obfuscate_project.py \
    /path/to/source \
    /path/to/target \
    --config config.yaml \
    --verbose \
    --skip-compile
```

---

## ⚙️ Konfiguration

### Konfigurationsdatei

Das Tool sucht automatisch nach:
1. `config.yaml` (bevorzugt)
2. `config.yml`
3. `config.json`

Im Verzeichnis, von dem das Tool ausgeführt wird.

### Wichtigste Einstellungen

#### `copyright_header_file`
Pfad zur Datei mit dem Copyright-Header-Template.

```yaml
copyright_header_file: "copyright_header.txt"
```

#### `obfuscate_folders`
Liste der Ordner, die obfusciert werden sollen (Kommentare entfernen + Umbenennung).

```yaml
obfuscate_folders:
  - "src"
  - "lib/Askoheat"
  - "include"
```

**Wichtig**: Nur diese Ordner werden obfusciert! Alle anderen bleiben unverändert.

#### `preserve_libraries`
Liste der Libraries, die NICHT obfusciert werden sollen.

```yaml
preserve_libraries:
  - "lib/ArduinoJson"
  - "lib/WiFi"
  - "lib/AsyncMqttClient-esphome"
  # ... alle externen Libraries
```

**Wichtig**: Alle `lib/*` Ordner außer deinen eigenen hier auflisten!

#### `copy_only_used_libraries`
Wenn `true`, werden nur tatsächlich verwendete Libraries kopiert.

```yaml
copy_only_used_libraries: true
```

**Empfehlung**: `true` (spart erheblich Speicherplatz)

#### `library_ignore_patterns`
Patterns für Dateien/Ordner, die aus Libraries entfernt werden sollen.

```yaml
library_ignore_patterns:
  - "examples"
  - "examples/**"
  - "test"
  - "tests"
  - "*.md"
  - "README*"
  - "LICENSE*"
```

**Effekt**: Reduziert Projektgröße um 50-80%!

### Vollständige Konfiguration

Siehe [CONFIG_GUIDE.md](CONFIG_GUIDE.md) für detaillierte Konfigurationsanleitung.

Beispiel `config.yaml`:
```yaml
copyright_header_file: "copyright_header.txt"
obfuscate_folders:
  - "src"
  - "lib/Askoheat"
  - "include"
copy_only_used_libraries: true
preserve_libraries:
  - "lib/ArduinoJson"
  - "lib/WiFi"
library_ignore_patterns:
  - "examples"
  - "*.md"
compile_after_obfuscation: true
verbose: false
variable_prefix: "v"
constant_prefix: "C"
```

---

## ⚙️ Funktionsweise

### Ablauf (v2.0)

```
┌──────────────────────────────────────────┐
│  1. Konfiguration laden                  │
│     - config.yaml / config.json          │
│     - copyright_header.txt               │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│  2. Dependency-Analyse                   │
│     - Scanne src/ nach #include          │
│     - Scanne lib/Askoheat nach #include  │
│     - Identifiziere verwendete Libraries │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│  3. Projektstruktur kopieren             │
│     - Root-Dateien (platformio.ini, etc.)│
│     - src/, include/, test/ Ordner       │
│     - Ignoriere .pio, .vscode, .git      │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│  4. Libraries kopieren (selektiv)        │
│     - Nur verwendete Libraries kopieren  │
│     - Entferne examples/, tests/, *.md   │
│     - Behalte nur Source-Dateien         │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│  5. Copyright-Header hinzufügen          │
│     - Nur lib/Askoheat Dateien           │
│     - Header vor Code einfügen           │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│  6. Dateien verarbeiten                  │
│     ┌─────────────────────────────────┐  │
│     │ Für obfuscate_folders:          │  │
│     │ - Kommentare entfernen          │  │
│     │ - Identifikatoren finden        │  │
│     │ - Code obfuscieren              │  │
│     └─────────────────────────────────┘  │
│     ┌─────────────────────────────────┐  │
│     │ Für preserve_libraries:         │  │
│     │ - Unverändert lassen            │  │
│     │ - Kommentare behalten           │  │
│     └─────────────────────────────────┘  │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│  7. Mapping speichern                    │
│     - JSON-Datei erstellen               │
│     - obfuscation_mapping.json           │
└────────────────┬─────────────────────────┘
                 │
                 ▼
┌──────────────────────────────────────────┐
│  8. Projekt kompilieren                  │
│     - 'pio run' ausführen                │
│     - Erfolg/Fehler berichten            │
└──────────────────────────────────────────┘
```

### Verarbeitete Dateitypen

Das Tool verarbeitet folgende Dateitypen:
- `.c` - C-Quelldateien
- `.cpp`, `.cc`, `.cxx` - C++-Quelldateien
- `.h`, `.hpp`, `.hxx` - Header-Dateien
- `.ino` - Arduino-Sketch-Dateien

### Ordner-basierte Verarbeitung (NEU in v2.0)

#### Obfuscierte Ordner
Diese Ordner werden vollständig obfusciert (konfigurierbar):
- `src/` - Haupt-Source-Code
- `lib/Askoheat/` - Eigene Library
- `include/` - Header-Dateien

**Verarbeitung**:
1. Copyright-Header hinzufügen (nur lib/Askoheat)
2. Kommentare entfernen
3. Variablen/Funktionen umbenennen

#### Geschützte Ordner (Preserve-Mode)
Diese Ordner bleiben unverändert:
- `lib/ArduinoJson/` (und alle anderen externen Libraries)
- Alle anderen nicht in `obfuscate_folders` aufgelisteten Ordner

**Verarbeitung**:
1. Nur kopieren
2. Kommentare bleiben erhalten
3. Variablennamen bleiben erhalten
4. Beispiele/Tests werden entfernt

### Geschützte Elemente

Das Tool schützt automatisch:

- **C/C++ Keywords**: `int`, `void`, `if`, `for`, `while`, etc.
- **Standard-Typen**: `uint8_t`, `size_t`, etc.
- **Arduino-Funktionen**: `pinMode`, `digitalWrite`, `Serial`, etc.
- **ESP32-Funktionen**: Standard ESP32 API
- **System-Funktionen**: Mit Unterstrich beginnende Identifier (`_xyz`)
- **Makros/Konstanten**: Vollständig in Großbuchstaben geschriebene Identifier (werden zu `C0`, `C1`, etc.)
- **Zusätzliche Words**: Konfigurierbar über `additional_reserved_words`

### Copyright-Header-System (NEU in v2.0)

#### Was wird hinzugefügt?
- Alle `.c`, `.cpp`, `.h`, `.hpp` Dateien in `lib/Askoheat/`
- Der Header wird VOR dem bestehenden Code eingefügt
- Der Header stammt aus `copyright_header.txt`

#### Beispiel:

**Vorher** (`lib/Askoheat/src/sensor.cpp`):
```cpp
#include "sensor.h"

void initSensor() {
    // Code...
}
```

**Nachher**:
```cpp
/*
 * ============================================================================
 * COPYRIGHT NOTICE
 * ============================================================================
 * Copyright (c) 2026 Dein Name
 * ...
 */

#include "sensor.h"

void v0() {
}
```

---

## 📊 Beispiele

### Vorher (Original-Code)

```cpp
// Temperature sensor configuration
#define MAX_TEMP 85
#define MIN_TEMP 15

// Initialize the temperature sensor
void initTemperatureSensor() {
    int sensorPin = 34;  // ADC1 Channel 6
    pinMode(sensorPin, INPUT);
    
    // Start reading
    float temperature = readTemperature(sensorPin);
    Serial.println(temperature);
}

/* 
 * Read temperature from sensor
 * Returns: Temperature in Celsius
 */
float readTemperature(int pin) {
    int rawValue = analogRead(pin);
    return (rawValue * 3.3) / 4095.0 * 100.0;
}
```

### Nachher (Obfusciert)

```cpp
#define C0 85
#define C1 15

void v0() {
    int v1 = 34;
    pinMode(v1, INPUT);
    
    float v2 = v3(v1);
    Serial.println(v2);
}

float v3(int v4) {
    int v5 = analogRead(v4);
    return (v5 * 3.3) / 4095.0 * 100.0;
}
```

### Mapping-Datei (obfuscation_mapping.json)

```json
{
  "MAX_TEMP": "C0",
  "MIN_TEMP": "C1",
  "initTemperatureSensor": "v0",
  "sensorPin": "v1",
  "temperature": "v2",
  "readTemperature": "v3",
  "pin": "v4",
  "rawValue": "v5"
}
```

---

## ⚠️ Wichtige Hinweise

### Einschränkungen

1. **Regex-basiert**: Das Tool verwendet reguläre Ausdrücke statt eines vollständigen C/C++ Parsers. In sehr komplexen Fällen können Probleme auftreten.

2. **Makros**: Komplexe Makros könnten teilweise nicht korrekt obfusciert werden.

3. **Externe Libraries**: Funktionen aus externen Libraries sollten in `RESERVED_WORDS` eingetragen werden, falls Probleme auftreten.

4. **Template-Code**: Sehr komplexer Template-Code könnte Probleme verursachen.

### Best Practices

- ✅ **Immer mit Verbose-Modus testen**: `--verbose` zeigt alle Änderungen an
- ✅ **Original-Projekt sichern**: Obwohl das Tool Kopien erstellt, immer ein Backup haben
- ✅ **Mapping-Datei aufbewahren**: Für Debugging und Rückübersetzung wichtig
- ✅ **Kompilierung prüfen**: Immer die automatische Kompilierung durchlaufen lassen
- ✅ **Schrittweise vorgehen**: Bei großen Projekten erst mit `--skip-compile` testen

### Sicherheit

⚠️ **WICHTIG**: Obfuscation ist **KEINE Verschlüsselung**!

- Der Code bleibt lesbar und dekompilierbar
- Es handelt sich nur um eine "Verschleierung", kein Kopierschutz
- Sensible Daten (Passwörter, API-Keys) müssen anderweitig geschützt werden

---

## 🔧 Troubleshooting

### Problem: "PlatformIO ist nicht installiert"

**Lösung:**
```bash
pip install platformio
# Oder
brew install platformio
```

### Problem: "Kompilierung fehlgeschlagen"

**Mögliche Ursachen:**

1. **Fehlende Library-Funktionen in RESERVED_WORDS**
   - Öffne `obfuscate_project.py`
   - Füge die fehlenden Funktionsnamen zu `RESERVED_WORDS` hinzu
   - Führe das Tool erneut aus

2. **Komplexe Makros**
   - Prüfe die Compiler-Fehler
   - Ggf. Makros manuell in der obfuscierten Version anpassen

3. **Template-Fehler**
   - Sehr komplexe Templates könnten Probleme verursachen
   - Manuelle Nachbearbeitung notwendig

**Debug-Strategie:**
```bash
# 1. Erstelle obfusciertes Projekt ohne Kompilierung
python3 obfuscate_project.py source target --skip-compile

# 2. Versuche manuell zu kompilieren
cd target
pio run

# 3. Analysiere Fehler und passe RESERVED_WORDS an
# 4. Wiederhole Schritt 1-3
```

### Problem: "Target existiert bereits"

Das Tool fragt nach Bestätigung. Bei Batch-Verarbeitung:
```bash
# Vorher manuell löschen
rm -rf target_path
python3 obfuscate_project.py source target
```

### Problem: "Zu viele/zu wenige Identifier obfusciert"

**Anpassung der RESERVED_WORDS:**

Bearbeite `obfuscate_project.py` und füge projektspezifische Funktionen hinzu:

```python
RESERVED_WORDS = {
    # ... bestehende Einträge ...
    'myLibraryFunction',
    'mySpecialVariable',
    # etc.
}
```

---

## 🔬 Technische Details

### Architektur

```
CodeObfuscator (Klasse)
├── __init__()
├── create_project_copy()      # Kopiert Projekt
├── remove_comments()           # Entfernt Kommentare
├── find_identifiers()          # Findet Identifikatoren
├── generate_obfuscated_name()  # Generiert neue Namen
├── obfuscate_identifiers()     # Ersetzt Identifikatoren
├── process_file()              # Verarbeitet eine Datei
├── process_all_files()         # Verarbeitet alle Dateien
├── save_mapping()              # Speichert Mapping
├── compile_project()           # Kompiliert mit PlatformIO
└── run()                       # Hauptablauf
```

### Algorithmus: Kommentar-Entfernung

```python
# Mehrzeilige Kommentare: /* ... */
content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

# Einzeilige Kommentare: //
# Mit String-Literal Protection (vereinfacht)
for line in lines:
    # Prüfe ob // in String-Literal
    # Entferne nur wenn außerhalb von Strings
```

### Algorithmus: Identifier-Ersetzung

1. **Finde alle Identifikatoren**: Regex `[a-zA-Z_][a-zA-Z0-9_]*`
2. **Filtere Keywords**: Entferne C/C++ Keywords und Standardfunktionen
3. **Sortiere nach Länge**: Längste zuerst (verhindert Teilstring-Probleme)
4. **Ersetze mit Word-Boundaries**: `\bidentifier\b` → nur ganze Wörter
5. **Generiere Namen**:
   - Normale Identifikatoren: `v0`, `v1`, `v2`, ...
   - Konstanten (UPPERCASE): `C0`, `C1`, `C2`, ...

### Performance

- **Kleine Projekte** (<100 Dateien): < 5 Sekunden
- **Mittlere Projekte** (100-500 Dateien): 5-30 Sekunden
- **Große Projekte** (>500 Dateien): 30+ Sekunden

Die Kompilierung nimmt meist den größten Teil der Zeit in Anspruch (2-10 Minuten).

### Dateigrößen

- **Original-Projekt**: Unverändert
- **Obfusciertes Projekt**: ~60-80% der Original-Größe (durch Kommentar-Entfernung)
- **Mapping-Datei**: ~1-10 KB (abhängig von der Anzahl der Identifikatoren)

---

## 📝 Erweiterte Nutzung

### Batch-Verarbeitung

```bash
#!/bin/bash
# batch_obfuscate.sh

PROJECTS=(
    "project1"
    "project2"
    "project3"
)

for project in "${PROJECTS[@]}"; do
    echo "Obfuscating $project..."
    python3 obfuscate_project.py \
        "/path/to/$project" \
        "/path/to/${project}-obfuscated" \
        --verbose
done
```

### Integration in CI/CD

```yaml
# .gitlab-ci.yml / .github/workflows/obfuscate.yml
obfuscate:
  script:
    - pip install platformio
    - python3 obfuscate_project.py . ./obfuscated
  artifacts:
    paths:
      - obfuscated/
```

### Anpassung für spezifische Projekte

Erstelle eine Wrapper-Datei `obfuscate_my_project.py`:

```python
#!/usr/bin/env python3
import sys
from obfuscate_project import CodeObfuscator

# Erweitere RESERVED_WORDS
from obfuscate_project import CodeObfuscator
CodeObfuscator.RESERVED_WORDS.update({
    'myCustomFunction1',
    'myCustomFunction2',
    # ... projektspezifische Funktionen
})

if __name__ == '__main__':
    obfuscator = CodeObfuscator(
        '/path/to/my/project',
        '/path/to/obfuscated',
        verbose=True
    )
    obfuscator.run()
```

---

## 🤝 Support & Contribution

### Probleme melden

Bei Problemen:
1. Prüfe die [Troubleshooting](#troubleshooting)-Sektion
2. Führe das Tool mit `--verbose` aus
3. Sammle Fehlerdetails und Compiler-Output

### Verbesserungen

Mögliche Erweiterungen:
- [ ] Vollständiger C/C++ Parser (z.B. mit `libclang`)
- [ ] Whitelist/Blacklist für Identifikatoren
- [ ] Verschiedene Obfuscation-Level
- [ ] GUI-Version
- [ ] Rückübersetzungs-Tool (De-Obfuscation für Debugging)

---

## 📄 Lizenz

Dieses Tool wurde automatisch generiert und steht zur freien Verwendung zur Verfügung.

---

## 📞 Kontakt

Erstellt am: 1. Juni 2026  
Version: 1.0.0  
Python: 3.7+

---

## 🎓 Glossar

- **Obfuscation**: Verschleierung von Code zur Erschwerung des Verständnisses
- **Identifier**: Bezeichner (Variablen, Funktionen, Klassen, etc.)
- **Reserved Words**: Reservierte Schlüsselwörter (z.B. `int`, `void`)
- **PlatformIO**: Build-System für Embedded-Entwicklung
- **Mapping**: Zuordnung Original-Name → Obfuscierter Name

---

**Ende der Dokumentation**

Viel Erfolg mit dem Tool! 🚀
