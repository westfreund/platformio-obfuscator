#!/bin/bash

# Beispiel-Script zur Verwendung des Obfuscators v2.0
# Passe die Pfade an dein Projekt an

SOURCE_PROJECT="/Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-main"
TARGET_PROJECT="/Users/andy/PlatformIO/GITLAB/askoheat_se_cpu-obfuscated"
CONFIG_FILE="config.yaml"

echo "=========================================="
echo "PlatformIO Project Obfuscator v2.0"
echo "=========================================="
echo ""
echo "Source:  $SOURCE_PROJECT"
echo "Target:  $TARGET_PROJECT"
echo "Config:  $CONFIG_FILE"
echo ""
echo "Neue Features in v2.0:"
echo "  ✓ Copyright-Header für lib/Kaninchen"
echo "  ✓ Nur verwendete Libraries werden kopiert"
echo "  ✓ Externe Libraries bleiben unverändert"
echo "  ✓ Beispiele/Tests werden automatisch entfernt"
echo ""
read -p "Fortfahren? (j/n): " confirm

if [ "$confirm" != "j" ]; then
    echo "Abgebrochen."
    exit 0
fi

# Prüfe ob Konfigurationsdatei existiert
if [ ! -f "$CONFIG_FILE" ]; then
    echo ""
    echo "⚠️  WARNUNG: $CONFIG_FILE nicht gefunden!"
    echo "Verwende Standard-Konfiguration..."
    echo ""
fi

# Ausführen des Obfuscators mit Konfiguration
python3 obfuscate_project.py "$SOURCE_PROJECT" "$TARGET_PROJECT" \
    --config "$CONFIG_FILE" \
    --verbose

echo ""
echo "=========================================="
echo "Fertig!"
echo "=========================================="
echo ""
echo "Obfusciertes Projekt: $TARGET_PROJECT"
echo "Mapping-Datei: $TARGET_PROJECT/obfuscation_mapping.json"
echo ""
echo "Prüfe Ergebnisse:"
echo "  - Copyright-Header: head -35 $TARGET_PROJECT/lib/Kaninchen/src/*.cpp"
echo "  - Externe Libraries: ls -la $TARGET_PROJECT/lib/"
echo "  - Projektgröße: du -sh $TARGET_PROJECT"
echo ""

