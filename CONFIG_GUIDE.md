# Konfigurations-Leitfaden

Vollständige Anleitung zur Konfiguration des PlatformIO Project Obfuscator v2.0.

---

## 📋 Inhaltsverzeichnis

- [Übersicht](#übersicht)
- [Konfigurationsdatei](#konfigurationsdatei)
- [Copyright-Header](#copyright-header)
- [Parameter-Referenz](#parameter-referenz)
- [Anwendungsbeispiele](#anwendungsbeispiele)
- [Erweiterte Szenarien](#erweiterte-szenarien)

---

## 🎯 Übersicht

Das Tool verwendet eine zentrale Konfigurationsdatei (`config.yaml` oder `config.json`), um alle Aspekte der Obfuscation zu steuern.

### Standard-Konfigurationsdatei

Das Tool sucht automatisch nach:
1. `config.yaml` (bevorzugt)
2. `config.yml`
3. `config.json`

Im Verzeichnis, von dem das Tool ausgeführt wird.

### Eigene Konfiguration angeben

```bash
python3 obfuscate_project.py source target --config my_config.yaml
```

---

## 📝 Konfigurationsdatei

### Vollständige config.yaml (mit Kommentaren)

```yaml
# ============================================================================
# PlatformIO Project Obfuscator v2.0 - Konfiguration
# ============================================================================

# Copyright-Header Einstellungen
# --------------------------------
# Pfad zur Textdatei mit dem Copyright-Header-Template
# Dieser Header wird ALLEN Dateien in lib/Askoheat vorangestellt
copyright_header_file: "copyright_header.txt"

# Obfuscation-Einstellungen
# --------------------------
# Dateitypen, die verarbeitet werden sollen
obfuscate_extensions:
  - .c      # C-Dateien
  - .cpp    # C++-Dateien
  - .cc     # C++-Dateien (alternative Endung)
  - .cxx    # C++-Dateien (alternative Endung)
  - .h      # Header-Dateien
  - .hpp    # C++-Header-Dateien
  - .hxx    # C++-Header-Dateien (alternative Endung)
  - .ino    # Arduino-Sketch-Dateien

# Ordner, die VOLLSTÄNDIG obfusciert werden sollen
# (Kommentare entfernen + Variablen/Funktionen umbenennen)
obfuscate_folders:
  - "src"           # Haupt-Source-Code
  - "lib/Askoheat"  # Eigene Library
  - "include"       # Header-Dateien

# Library-Handling
# ----------------
# Wenn true: Nur tatsächlich verwendete Libraries werden kopiert
# Wenn false: Alle Libraries werden kopiert
copy_only_used_libraries: true

# Libraries, die NICHT obfusciert werden
# (Diese werden kopiert, aber Kommentare und Namen bleiben erhalten)
# WICHTIG: Alle lib/* Ordner außer Askoheat hier auflisten!
preserve_libraries:
  - "lib/Adafruit_ADS1X15"
  - "lib/Adafruit-MCP23008"
  - "lib/ArduinoJson"
  - "lib/arduinoWebSockets"
  - "lib/AsyncMqttClient-esphome"
  - "lib/AsyncTCP-esphome"
  - "lib/ConfigManager"
  - "lib/EEPROM"
  - "lib/esp32_https_server"
  - "lib/ESP32Ping"
  - "lib/ESP32SSDP"
  - "lib/ESPAsyncTCP-esphome"
  - "lib/ESPAsyncWebServer"
  - "lib/ESPPerfectTime"
  - "lib/MCP23017"
  - "lib/nvs_flash"
  - "lib/Preferences"
  - "lib/tinyxml2-master"
  - "lib/U8g2"
  - "lib/Update"
  - "lib/WiFi"

# Patterns für Dateien/Ordner, die aus Libraries entfernt werden sollen
# (Reduziert Projektgröße erheblich)
library_ignore_patterns:
  - "examples"        # Beispiel-Code
  - "examples/**"     # Alle Dateien in examples/
  - "test"            # Test-Code
  - "tests"           # Test-Code (alternative Benennung)
  - "test/**"         # Alle Dateien in test/
  - "tests/**"        # Alle Dateien in tests/
  - "docs"            # Dokumentation
  - "doc"             # Dokumentation (alternative Benennung)
  - "documentation"   # Dokumentation (alternative Benennung)
  - "*.md"            # Markdown-Dateien
  - "README*"         # README-Dateien
  - "LICENSE*"        # Lizenz-Dateien
  - "CHANGELOG*"      # Changelog-Dateien
  - ".git"            # Git-Repository
  - ".github"         # GitHub-Konfiguration
  - ".vscode"         # VS Code Einstellungen
  - "*.pdf"           # PDF-Dateien
  - "*.png"           # Bilder
  - "*.jpg"           # Bilder
  - "*.jpeg"          # Bilder

# Projekt-Kopier-Einstellungen
# -----------------------------
# Ordner/Dateien, die beim Kopieren des Hauptprojekts ignoriert werden
project_ignore_patterns:
  - ".pio"            # PlatformIO Build-Ordner
  - ".vscode"         # VS Code Einstellungen
  - ".git"            # Git-Repository
  - "__pycache__"     # Python Cache
  - "*.pyc"           # Python Bytecode
  - ".DS_Store"       # macOS Dateisystem-Metadaten

# Kompilierungs-Einstellungen
# ----------------------------
# Nach der Obfuscation automatisch kompilieren?
compile_after_obfuscation: true

# Timeout für Kompilierung in Sekunden
# (600 Sekunden = 10 Minuten)
compilation_timeout: 600

# Output-Einstellungen
# --------------------
# Ausführliche Ausgabe aktivieren (überschrieben durch --verbose)
verbose: false

# Name der JSON-Mapping-Datei (Original → Obfusciert)
mapping_file: "obfuscation_mapping.json"

# Erweiterte Einstellungen
# -------------------------
# Zusätzliche Funktionen/Variablen, die NICHT umbenannt werden sollen
# (Werden zu den Standard RESERVED_WORDS hinzugefügt)
additional_reserved_words: []
  # Beispiel:
  # - "myCustomFunction"
  # - "specialVariable"
  # - "CUSTOM_CONSTANT"

# Prefix für obfuscierte normale Variablen/Funktionen
# Standard: "v" → v0, v1, v2, ...
variable_prefix: "v"

# Prefix für obfuscierte Konstanten (UPPERCASE)
# Standard: "C" → C0, C1, C2, ...
constant_prefix: "C"
```

---

## 📄 Copyright-Header

### copyright_header.txt anpassen

Die Datei `copyright_header.txt` enthält den Header, der allen Dateien in `lib/Askoheat` vorangestellt wird.

#### Standard-Template:

```c
/*
 * ============================================================================
 * COPYRIGHT NOTICE
 * ============================================================================
 * 
 * Copyright (c) 2026 [Dein Firmenname / Dein Name]
 * All rights reserved.
 * 
 * This software is proprietary and confidential.
 * Unauthorized copying, modification, distribution, or use of this software,
 * via any medium, is strictly prohibited without express written permission.
 * 
 * Contact: [deine-email@example.com]
 * Website: [www.example.com]
 * 
 * ============================================================================
 * DISCLAIMER
 * ============================================================================
 * 
 * THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 * 
 * ============================================================================
 */

```

#### Anpassungen:

Ersetze:
- `[Dein Firmenname / Dein Name]` → Dein Name oder Firmenname
- `[deine-email@example.com]` → Deine E-Mail-Adresse
- `[www.example.com]` → Deine Website
- Copyright-Jahr nach Bedarf
- Lizenztext nach Bedarf

#### Alternative Lizenz-Templates:

**MIT-Style:**
```c
/*
 * Copyright (c) 2026 Dein Name
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software [...]
 */
```

**GPL-Style:**
```c
/*
 * Copyright (C) 2026 Dein Name
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License [...]
 */
```

**Proprietär (geschlossen):**
```c
/*
 * PROPRIETARY AND CONFIDENTIAL
 * Copyright (c) 2026 Dein Unternehmen. All Rights Reserved.
 * 
 * NOTICE: All information contained herein is, and remains
 * the property of [Dein Unternehmen].
 */
```

---

## 🔧 Parameter-Referenz

### Wichtigste Parameter im Detail

#### `copyright_header_file`
- **Typ**: String (Dateipfad)
- **Standard**: `"copyright_header.txt"`
- **Beschreibung**: Pfad zur Textdatei mit dem Copyright-Header-Template
- **Beispiel**: `"headers/my_copyright.txt"`

#### `obfuscate_folders`
- **Typ**: Liste von Strings
- **Standard**: `["src", "lib/Askoheat", "include"]`
- **Beschreibung**: Nur Dateien in diesen Ordnern werden obfusciert
- **Beispiel**: 
  ```yaml
  obfuscate_folders:
    - "src"
    - "lib/MyLib"
  ```

#### `copy_only_used_libraries`
- **Typ**: Boolean
- **Standard**: `true`
- **Beschreibung**: Wenn `true`, werden nur tatsächlich verwendete Libraries kopiert
- **Empfehlung**: `true` (spart Speicherplatz)

#### `preserve_libraries`
- **Typ**: Liste von Strings
- **Standard**: Alle externen Libraries
- **Beschreibung**: Libraries in dieser Liste werden NICHT obfusciert
- **Wichtig**: Alle lib/* Ordner außer deinen eigenen hier auflisten!

#### `library_ignore_patterns`
- **Typ**: Liste von Strings (Glob-Patterns)
- **Standard**: Siehe config.yaml
- **Beschreibung**: Dateien/Ordner, die aus Libraries entfernt werden
- **Glob-Patterns**: 
  - `*.md` = Alle Markdown-Dateien
  - `examples/**` = Alle Dateien im examples-Ordner
  - `README*` = Alle Dateien die mit README beginnen

#### `additional_reserved_words`
- **Typ**: Liste von Strings
- **Standard**: `[]`
- **Beschreibung**: Zusätzliche Funktionen/Variablen, die nicht umbenannt werden
- **Beispiel**:
  ```yaml
  additional_reserved_words:
    - "myImportantFunction"
    - "CRITICAL_CONSTANT"
  ```

#### `variable_prefix` / `constant_prefix`
- **Typ**: String
- **Standard**: `"v"` / `"C"`
- **Beschreibung**: Prefixe für obfuscierte Namen
- **Beispiel**: 
  ```yaml
  variable_prefix: "x"   # → x0, x1, x2, ...
  constant_prefix: "K"   # → K0, K1, K2, ...
  ```

---

## 💡 Anwendungsbeispiele

### Beispiel 1: Minimale Konfiguration

**Szenario**: Nur das Nötigste konfigurieren

```yaml
copyright_header_file: "my_header.txt"
obfuscate_folders:
  - "src"
  - "lib/Askoheat"
```

Alles andere nutzt Standard-Werte.

### Beispiel 2: Alle Libraries kopieren

**Szenario**: Alle Libraries sollen vollständig kopiert werden (ohne Filtering)

```yaml
copy_only_used_libraries: false
library_ignore_patterns: []
```

### Beispiel 3: Mehr Ordner obfuscieren

**Szenario**: Auch `test/` Ordner soll obfusciert werden

```yaml
obfuscate_folders:
  - "src"
  - "lib/Askoheat"
  - "include"
  - "test"
```

### Beispiel 4: Kein Copyright-Header

**Szenario**: Kein Copyright-Header hinzufügen

```yaml
copyright_header_file: ""
```

Oder lösche die Datei `copyright_header.txt`.

### Beispiel 5: Eigene Reserved Words

**Szenario**: Bestimmte Funktionen sollen nicht umbenannt werden

```yaml
additional_reserved_words:
  - "myCallback"
  - "customInit"
  - "IMPORTANT_FLAG"
```

### Beispiel 6: Andere Prefixe

**Szenario**: Obfuscierte Namen sollen anders aussehen

```yaml
variable_prefix: "var"   # → var0, var1, var2
constant_prefix: "CONST" # → CONST0, CONST1, CONST2
```

---

## 🚀 Erweiterte Szenarien

### Multi-Library-Projekt

**Problem**: Mehrere eigene Libraries, die obfusciert werden sollen

**Lösung**:
```yaml
obfuscate_folders:
  - "src"
  - "lib/MyLib1"
  - "lib/MyLib2"
  - "lib/MyLib3"
  - "include"

# Nur externe Libraries in preserve_libraries auflisten
preserve_libraries:
  - "lib/ArduinoJson"
  - "lib/WiFi"
  # ... aber NICHT MyLib1, MyLib2, MyLib3
```

### Projekt ohne externe Libraries

**Problem**: Nur eigener Code, keine externen Libraries

**Lösung**:
```yaml
copy_only_used_libraries: false
preserve_libraries: []
obfuscate_folders:
  - "src"
  - "lib"  # Alle Libraries obfuscieren
  - "include"
```

### Sehr große Projekte

**Problem**: Kompilierung dauert sehr lange

**Lösung**:
```yaml
compilation_timeout: 1800  # 30 Minuten
compile_after_obfuscation: false  # Optional: Manuell kompilieren
```

Dann manuell kompilieren:
```bash
python3 obfuscate_project.py source target --skip-compile
cd target
pio run
```

### Debug-Modus

**Problem**: Tool funktioniert nicht wie erwartet

**Lösung**:
```yaml
verbose: true
```

Oder per Kommandozeile:
```bash
python3 obfuscate_project.py source target --verbose
```

### JSON statt YAML

**Problem**: Kein PyYAML installiert

**Lösung**: Verwende `config.json` statt `config.yaml`

```json
{
  "copyright_header_file": "copyright_header.txt",
  "obfuscate_folders": ["src", "lib/Askoheat", "include"],
  "copy_only_used_libraries": true,
  "verbose": false
}
```

---

## 📊 Konfiguration testen

### Schritt 1: Dry-Run ohne Kompilierung

```bash
python3 obfuscate_project.py source target --skip-compile --verbose
```

Prüfe:
- Wurden die richtigen Libraries kopiert?
- Wurden Beispiele herausgefiltert?
- Wurde der Copyright-Header hinzugefügt?
- Wurden die richtigen Dateien obfusciert?

### Schritt 2: Mit Kompilierung

```bash
python3 obfuscate_project.py source target --verbose
```

Prüfe:
- Kompiliert das Projekt erfolgreich?
- Falls nicht: Welche Fehler gibt es?

### Schritt 3: Anpassen

Falls Probleme auftreten:
1. Füge fehlende Funktionen zu `additional_reserved_words` hinzu
2. Passe `obfuscate_folders` an
3. Prüfe `preserve_libraries`

---

## ⚠️ Häufige Fehler

### Fehler: "Library XYZ nicht gefunden"

**Ursache**: Library wird verwendet, aber nicht kopiert

**Lösung**: 
- Setze `copy_only_used_libraries: false`
- Oder füge Library manuell hinzu

### Fehler: "Funktion ABC nicht gefunden" (Compiler)

**Ursache**: Wichtige Funktion wurde umbenannt

**Lösung**: Füge zu `additional_reserved_words` hinzu
```yaml
additional_reserved_words:
  - "ABC"
```

### Fehler: "Copyright-Header fehlt"

**Ursache**: Datei `copyright_header.txt` nicht gefunden

**Lösung**: 
- Prüfe Pfad in `copyright_header_file`
- Stelle sicher, dass Datei existiert

---

## 📞 Zusammenfassung

Die wichtigsten Einstellungen für den Einstieg:

```yaml
# Pflicht
copyright_header_file: "copyright_header.txt"
obfuscate_folders: ["src", "lib/Askoheat"]

# Empfohlen
copy_only_used_libraries: true
compile_after_obfuscation: true
verbose: false
```

**Nächste Schritte**:
1. Passe `copyright_header.txt` an
2. Passe `config.yaml` an
3. Teste mit `--skip-compile --verbose`
4. Teste mit Kompilierung

---

**Weitere Hilfe**: Siehe [README.md](README.md) und [CHANGELOG.md](CHANGELOG.md)
