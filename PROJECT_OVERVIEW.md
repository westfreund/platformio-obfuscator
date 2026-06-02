# PlatformIO Project Obfuscator - Projektübersicht

## 📁 Projektstruktur

```
code-obfuscator/
├── obfuscate_project.py    # ⭐ Haupt-Tool (Python-Script)
├── README.md               # 📖 Ausführliche Dokumentation
├── QUICKSTART.md           # 🚀 Schnelleinstieg-Anleitung
├── example_usage.sh        # 💡 Beispiel-Script zur Verwendung
├── requirements.txt        # 📦 Python-Dependencies (keine extern!)
├── .gitignore             # 🚫 Git-Ignore-Regeln
└── PROJECT_OVERVIEW.md    # 📋 Diese Datei
```

## 🎯 Was macht dieses Tool?

Dieses Tool ermöglicht die **automatische Code-Obfuscation** von PlatformIO-Projekten für die Veröffentlichung:

1. ✅ **Kommentare entfernen** - Alle `//` und `/* */` Kommentare werden entfernt
2. ✅ **Code obfuscieren** - Variablen und Funktionen werden durch generische Namen ersetzt
3. ✅ **Projekt kopieren** - Das Original bleibt unverändert
4. ✅ **Kompilierung prüfen** - Automatische Verifikation mit PlatformIO

## 🚀 Schnellstart

```bash
# 1. Ins Tool-Verzeichnis wechseln
cd /Users/andy/PlatformIO/GITLAB/code-obfuscator

# 2. Tool ausführen
python3 obfuscate_project.py \
    /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-main \
    /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated

# 3. Ergebnis prüfen
cat /Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated/obfuscation_mapping.json
```

## 📚 Dokumentation

| Datei | Beschreibung | Wann verwenden? |
|-------|-------------|----------------|
| [README.md](README.md) | Vollständige Dokumentation | Für alle Details, Troubleshooting, Beispiele |
| [QUICKSTART.md](QUICKSTART.md) | Schnelleinstieg | Für sofortigen Start mit Beispielen |
| `--help` | Kommandozeilen-Hilfe | `python3 obfuscate_project.py --help` |

## 🔑 Hauptfunktionen

### 1. obfuscate_project.py

Das Haupt-Python-Script mit folgenden Features:

- **Kommentar-Entfernung**
  - Einzeilige (`//`) und mehrzeilige (`/* */`) Kommentare
  - String-Literal Protection
  
- **Code-Obfuscation**
  - Intelligente Identifier-Erkennung
  - Schutz von C/C++ Keywords
  - Schutz von Arduino/ESP32 Funktionen
  - Generierung von Mapping-Datei
  
- **PlatformIO-Integration**
  - Automatische Kompilierung
  - Build-Verifikation
  - Fehlerbehandlung

### 2. Kommandozeilen-Parameter

```
python3 obfuscate_project.py <source> <target> [optionen]

Positional:
  source              Quellpfad des PlatformIO-Projekts
  target              Zielpfad für das obfuscierte Projekt

Optional:
  -v, --verbose       Ausführliche Ausgabe
  -s, --skip-compile  Kompilierung überspringen
  -h, --help          Hilfe anzeigen
```

## 📊 Beispiel-Transformation

### Vorher:
```cpp
// Initialize sensor
void initSensor() {
    int pin = 34;  // ADC pin
    pinMode(pin, INPUT);
}
```

### Nachher:
```cpp
void v0() {
    int v1 = 34;
    pinMode(v1, INPUT);
}
```

### Mapping (obfuscation_mapping.json):
```json
{
  "initSensor": "v0",
  "pin": "v1"
}
```

## ⚙️ Technische Details

### Verwendete Python-Module
- Standard-Library only! Keine externen Dependencies
- `os`, `sys`, `re`, `shutil`, `subprocess`, `argparse`, `json`, `pathlib`, `typing`, `hashlib`

### Unterstützte Dateitypen
- `.c`, `.cpp`, `.cc`, `.cxx` - C/C++ Quelldateien
- `.h`, `.hpp`, `.hxx` - Header-Dateien
- `.ino` - Arduino Sketches

### Geschützte Elemente
- C/C++ Keywords (`int`, `void`, `for`, etc.)
- Standard-Typen (`uint8_t`, `size_t`, etc.)
- Arduino-Funktionen (`pinMode`, `digitalWrite`, etc.)
- ESP32-API
- System-Funktionen (mit `_` Prefix)

## 🔧 Anpassung

### RESERVED_WORDS erweitern

Falls bestimmte Funktionen nicht umbenannt werden sollen, bearbeite `obfuscate_project.py`:

```python
RESERVED_WORDS = {
    # ... bestehende Einträge ...
    'meineFunktion',
    'meineVariable',
    # etc.
}
```

### Batch-Verarbeitung

Verwende `example_usage.sh` als Vorlage:

```bash
chmod +x example_usage.sh
./example_usage.sh
```

## 📈 Performance

| Projektgröße | Verarbeitungszeit | Kompilierungszeit |
|--------------|-------------------|-------------------|
| Klein (<100 Dateien) | < 5 Sek. | 2-5 Min. |
| Mittel (100-500 Dateien) | 5-30 Sek. | 5-10 Min. |
| Groß (>500 Dateien) | 30+ Sek. | 10+ Min. |

## ⚠️ Wichtige Hinweise

### Sicherheit
- **Obfuscation ≠ Verschlüsselung**
- Code bleibt lesbar und dekompilierbar
- Sensible Daten müssen anderweitig geschützt werden

### Einschränkungen
- Regex-basierte Lösung (kein vollständiger C/C++ Parser)
- Komplexe Makros können Probleme verursachen
- Sehr komplexer Template-Code könnte Fehler verursachen

### Best Practices
- ✅ Immer mit `--verbose` testen
- ✅ Original-Projekt sichern
- ✅ Mapping-Datei aufbewahren
- ✅ Kompilierung prüfen lassen
- ✅ Bei großen Projekten erst mit `--skip-compile` testen

## 🐛 Troubleshooting

### "PlatformIO nicht gefunden"
```bash
pip install platformio
```

### "Kompilierung fehlgeschlagen"
```bash
# Ohne Kompilierung ausführen
python3 obfuscate_project.py source target --skip-compile

# Manuell kompilieren und Fehler analysieren
cd target
pio run

# RESERVED_WORDS in obfuscate_project.py erweitern
```

### "Zu viele Identifier umbenannt"
→ Erweitere `RESERVED_WORDS` im Script

## 📝 Workflow

```
1. Projekt-Kopie erstellen
   ↓
2. Kommentare entfernen
   ↓
3. Identifikatoren finden
   ↓
4. Code obfuscieren
   ↓
5. Mapping speichern
   ↓
6. Mit PlatformIO kompilieren
   ↓
7. Erfolg/Fehler berichten
```

## 🎓 Nächste Schritte

1. **Erste Verwendung**: Siehe [QUICKSTART.md](QUICKSTART.md)
2. **Details & Beispiele**: Siehe [README.md](README.md)
3. **Anpassen**: Bearbeite `obfuscate_project.py` nach Bedarf
4. **Automatisieren**: Nutze `example_usage.sh` als Vorlage

## 📞 Version

- **Version**: 1.0.0
- **Erstellt**: 1. Juni 2026
- **Python**: 3.7+
- **PlatformIO**: Beliebige Version

---

**Bereit zum Start? 🚀**

```bash
python3 obfuscate_project.py --help
```

---

Ende der Übersicht.
