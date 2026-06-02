# Changelog - PlatformIO Project Obfuscator

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

---

## [2.0.0] - 2026-06-02

### ✨ Neue Features

#### Copyright-Header-Funktion
- **Copyright-Header für lib/Askoheat**: Alle Dateien im `lib/Askoheat` Ordner erhalten automatisch einen konfigurierbaren Copyright-Header
- **Template-System**: Der Copyright-Header wird aus einer externen Textdatei geladen (`copyright_header.txt`)
- **Vollständig anpassbar**: Firmennamen, Kontaktdaten, Lizenzbedingungen können frei konfiguriert werden

#### Selektive Library-Verarbeitung
- **Dependency-Analyse**: Das Tool analysiert automatisch, welche Libraries tatsächlich im Projekt verwendet werden
- **Intelligentes Kopieren**: Nur verwendete Libraries werden kopiert (konfigurierbar)
- **Keine Beispiele**: Beispiel-Code, Tests, Dokumentation werden automatisch aus Libraries entfernt
- **Preserve-Modus**: Libraries außer `lib/Askoheat` werden NICHT obfusciert - Kommentare und Variablennamen bleiben erhalten
- **Pattern-basiertes Filtern**: Konfigurierbare Ignore-Patterns für unerwünschte Dateien

#### Konfigurationssystem
- **YAML-Unterstützung**: Umfassende Konfigurationsdatei `config.yaml` für alle Einstellungen
- **JSON-Fallback**: Alternativ kann auch JSON verwendet werden
- **Flexible Ordner-Konfiguration**: Definiere selbst, welche Ordner obfusciert werden sollen
- **Library-Whitelist**: Liste der Libraries, die nicht obfusciert werden sollen
- **Anpassbare Prefixe**: Variable und Konstanten-Prefixe sind konfigurierbar

#### Erweiterte Verarbeitung
- **Ordner-basierte Obfuscation**: Nur definierte Ordner (`src`, `lib/Askoheat`, `include`) werden obfusciert
- **Preservation-Mode**: Externe Libraries bleiben lesbar und wartbar
- **Zusätzliche Reserved Words**: Projektspezifische Funktionen können geschützt werden

### 🔧 Verbesserungen

- **Verbesserte Performance**: Optimierte Dependency-Analyse
- **Besseres Logging**: Detailliertere Ausgabe im Verbose-Modus
- **Robustere Fehlerbehandlung**: Bessere Error-Messages und Fallback-Mechanismen
- **Modulare Architektur**: Code in Config- und Obfuscator-Klassen aufgeteilt

### 📝 Konfigurationsoptionen

Neue Konfigurationsparameter in `config.yaml`:

```yaml
copyright_header_file: "copyright_header.txt"
obfuscate_folders: ["src", "lib/Askoheat", "include"]
copy_only_used_libraries: true
preserve_libraries: [...]
library_ignore_patterns: ["examples", "*.md", ...]
additional_reserved_words: []
variable_prefix: "v"
constant_prefix: "C"
```

### 💻 Kommandozeilen-Änderungen

Neue Parameter:
- `--config CONFIG` oder `-c CONFIG`: Pfad zur Konfigurationsdatei

### 📖 Dokumentation

- README.md erweitert mit neuen Features
- QUICKSTART.md aktualisiert
- Neue Datei: CHANGELOG.md (diese Datei)
- Neue Datei: CONFIG_GUIDE.md (Konfigurations-Leitfaden)
- Beispiel-Konfiguration: config.yaml
- Beispiel-Copyright-Header: copyright_header.txt

### 🔄 Migration von v1.0 zu v2.0

**Wichtig**: Version 2.0 verhält sich anders als Version 1.0!

#### Hauptunterschiede:

1. **Selektive Library-Kopie**:
   - v1.0: Kopierte alle Libraries vollständig
   - v2.0: Kopiert nur verwendete Libraries, filtert Beispiele heraus

2. **Library-Obfuscation**:
   - v1.0: Obfuscierte ALLE Dateien
   - v2.0: Obfusciert nur `src/`, `include/` und `lib/Askoheat/`

3. **Copyright-Header**:
   - v1.0: Keine Copyright-Header
   - v2.0: Automatische Copyright-Header für `lib/Askoheat/`

#### Upgrade-Anleitung:

1. **Alte Version sichern**:
   ```bash
   cp obfuscate_project_v1.py.backup obfuscate_project_v1.py
   ```

2. **Konfigurationsdatei anpassen**:
   - Passe `config.yaml` an dein Projekt an
   - Bearbeite `copyright_header.txt` mit deinen Daten

3. **Testlauf mit neuer Version**:
   ```bash
   python3 obfuscate_project.py source target --verbose --skip-compile
   ```

4. **Vergleiche Ergebnis**:
   - Prüfe ob alle Libraries korrekt kopiert wurden
   - Prüfe ob Copyright-Header korrekt hinzugefügt wurden

#### Rückfall auf v1.0:

Falls v2.0 Probleme macht, verwende die alte Version:
```bash
python3 obfuscate_project_v1.py.backup source target
```

### ⚠️ Breaking Changes

- **Kommandozeilen-Parameter**: Neuer optionaler Parameter `--config`
- **Verhalten**: Libraries werden standardmäßig anders behandelt
- **Output**: Zusätzliche Dateien im Zielordner (obfuscation_mapping.json)

---

## [1.0.0] - 2026-06-01

### Initiale Version

- ✅ Kommentar-Entfernung (einzeilig und mehrzeilig)
- ✅ Code-Obfuscation (Variablen und Funktionen)
- ✅ PlatformIO-Kompilierung
- ✅ Mapping-Datei
- ✅ Verbose-Modus
- ✅ Skip-Compile-Option
- ✅ Vollständige Projekt-Kopie

---

## Changelog-Format

Dieses Changelog folgt dem Format von [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

Versionsnummern folgen [Semantic Versioning](https://semver.org/lang/de/):
- **MAJOR**: Inkompatible API-Änderungen
- **MINOR**: Neue Features (rückwärtskompatibel)
- **PATCH**: Bugfixes (rückwärtskompatibel)

---

**Weitere Informationen**: Siehe [README.md](README.md)
