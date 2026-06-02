# GitLab Veröffentlichungs-Anleitung

## 🚀 Projekt auf GitLab veröffentlichen

Dieses Dokument führt dich Schritt für Schritt durch die Veröffentlichung des PlatformIO Project Obfuscator auf GitLab.

---

## ✅ Bereits erledigt

- ✅ Git-Repository initialisiert
- ✅ Alle Dateien hinzugefügt
- ✅ Initial Commit erstellt (13 Dateien, 3830+ Zeilen)
- ✅ `.gitignore` konfiguriert

---

## 📋 Nächste Schritte

### Schritt 1: GitLab-Repository erstellen

#### Option A: Über GitLab Webseite

1. **Öffne GitLab**: https://gitlab.com
2. **Login** mit deinem Account
3. **Klicke** auf "New project" (grüner Button oben rechts)
4. **Wähle** "Create blank project"
5. **Fülle aus**:
   - **Project name**: `platformio-obfuscator`
   - **Project slug**: `platformio-obfuscator` (automatisch)
   - **Visibility Level**: 
     - 🔒 **Private** (empfohlen für proprietären Code)
     - 🌍 **Public** (wenn Open Source)
   - **Initialize repository**: ❌ **NICHT** auswählen (wir haben schon ein Repo)
6. **Klicke** "Create project"

#### Option B: Mit GitLab CLI (glab)

```bash
# Falls glab noch nicht installiert:
# brew install glab

# Repository erstellen
glab repo create platformio-obfuscator \
    --description "PlatformIO Project Obfuscator - Code obfuscation tool with copyright header system" \
    --private  # oder --public für öffentlich
```

---

### Schritt 2: Git-Konfiguration (optional, aber empfohlen)

```bash
# Git-Benutzer konfigurieren (falls noch nicht geschehen)
git config --global user.name "Dein Name"
git config --global user.email "deine-email@example.com"

# Oder nur für dieses Repository
git config user.name "Dein Name"
git config user.email "deine-email@example.com"

# Commit-Autor korrigieren (optional)
git commit --amend --reset-author --no-edit
```

---

### Schritt 3: Remote hinzufügen

Nach dem Erstellen des GitLab-Repositories, kopiere die Repository-URL aus GitLab.

#### SSH (empfohlen):
```bash
cd /Users/andy/PlatformIO/GITLAB/code-obfuscator

git remote add origin git@gitlab.com:DEIN_USERNAME/platformio-obfuscator.git
```

#### HTTPS (alternative):
```bash
cd /Users/andy/PlatformIO/GITLAB/code-obfuscator

git remote add origin https://gitlab.com/DEIN_USERNAME/platformio-obfuscator.git
```

**Ersetze `DEIN_USERNAME` mit deinem GitLab-Benutzernamen!**

---

### Schritt 4: Code zu GitLab pushen

```bash
cd /Users/andy/PlatformIO/GITLAB/code-obfuscator

# Main Branch benennen (GitLab Standard)
git branch -M main

# Code hochladen
git push -u origin main
```

Bei SSH-Verwendung: Falls Authentifizierung fehlschlägt, musst du deinen SSH-Key zu GitLab hinzufügen.

Bei HTTPS-Verwendung: Du wirst nach Benutzername und Passwort/Token gefragt.

---

## 🔑 SSH-Key einrichten (falls noch nicht vorhanden)

### SSH-Key generieren

```bash
# Prüfe ob bereits ein SSH-Key existiert
ls -la ~/.ssh/id_*.pub

# Falls nicht, erstelle einen neuen
ssh-keygen -t ed25519 -C "deine-email@example.com"
# Drücke Enter für Standard-Speicherort
# Optional: Passphrase eingeben

# Zeige den öffentlichen Key an
cat ~/.ssh/id_ed25519.pub
```

### SSH-Key zu GitLab hinzufügen

1. **Kopiere** den Inhalt von `cat ~/.ssh/id_ed25519.pub`
2. **Öffne** GitLab: https://gitlab.com
3. **Gehe zu**: Dein Profil → Preferences → SSH Keys
4. **Füge** den Key ein:
   - **Key**: (kopierter SSH-Key)
   - **Title**: "MacBook Air" (oder ein anderer Name)
   - **Expires**: Optional (z.B. 1 Jahr)
5. **Klicke** "Add key"

### SSH-Verbindung testen

```bash
ssh -T git@gitlab.com
```

Erwartete Ausgabe: `Welcome to GitLab, @DEIN_USERNAME!`

---

## 📝 GitLab Personal Access Token (für HTTPS)

Falls du HTTPS verwendest:

1. **Öffne** GitLab: https://gitlab.com
2. **Gehe zu**: Dein Profil → Preferences → Access Tokens
3. **Erstelle** neuen Token:
   - **Token name**: "git-access"
   - **Scopes**: ✅ `write_repository`, ✅ `read_repository`
   - **Expires**: Optional
4. **Klicke** "Create personal access token"
5. **Kopiere** den Token (wird nur einmal angezeigt!)
6. **Verwende** den Token als Passwort beim `git push`

---

## 🎯 Zusammengefasste Befehle (Copy-Paste)

### Variante A: SSH (empfohlen)

```bash
cd /Users/andy/PlatformIO/GITLAB/code-obfuscator

# Remote hinzufügen (ERSETZE DEIN_USERNAME!)
git remote add origin git@gitlab.com:DEIN_USERNAME/platformio-obfuscator.git

# Branch benennen
git branch -M main

# Pushen
git push -u origin main
```

### Variante B: HTTPS

```bash
cd /Users/andy/PlatformIO/GITLAB/code-obfuscator

# Remote hinzufügen (ERSETZE DEIN_USERNAME!)
git remote add origin https://gitlab.com/DEIN_USERNAME/platformio-obfuscator.git

# Branch benennen
git branch -M main

# Pushen (du wirst nach Credentials gefragt)
git push -u origin main
```

---

## 🔍 Verifizierung

Nach erfolgreichem Push:

1. **Öffne** dein GitLab-Repository: https://gitlab.com/DEIN_USERNAME/platformio-obfuscator
2. **Prüfe**:
   - ✅ Alle 13 Dateien sind sichtbar
   - ✅ README.md wird schön formatiert angezeigt
   - ✅ Commit-Message ist korrekt
   - ✅ Alle Markdown-Dateien sind lesbar

---

## 📦 Repository-Beschreibung für GitLab

Wenn du die Repository-Beschreibung auf GitLab bearbeiten möchtest:

**Kurzbeschreibung:**
```
PlatformIO Project Obfuscator v2.0 - Code obfuscation tool with copyright header system, selective library processing, and YAML configuration
```

**Tags:**
- `platformio`
- `obfuscation`
- `code-protection`
- `esp32`
- `arduino`
- `copyright`
- `python`

---

## 🛡️ Empfohlene GitLab-Einstellungen

### Visibility & Permissions

- **Visibility**: Private (für proprietären Code)
- **Repository**: 
  - ✅ Enable "Issues"
  - ✅ Enable "Wiki"
  - ❌ Disable "Merge Requests" (falls alleiniger Entwickler)

### Protected Branches

- **Branch**: `main`
  - ✅ Protected
  - Allowed to push: Maintainers only
  - Allowed to merge: Maintainers only

---

## 🔄 Zukünftige Updates

Wenn du Änderungen am Code machst:

```bash
cd /Users/andy/PlatformIO/GITLAB/code-obfuscator

# Änderungen ansehen
git status

# Änderungen hinzufügen
git add .

# Commit erstellen
git commit -m "Deine Commit-Nachricht"

# Zu GitLab pushen
git push
```

---

## 🆘 Problemlösung

### Problem: "Permission denied (publickey)"

**Lösung**: SSH-Key zu GitLab hinzufügen (siehe oben)

### Problem: "Authentication failed" (HTTPS)

**Lösung**: 
- Verwende Personal Access Token statt Passwort
- Oder wechsle zu SSH

### Problem: "Remote already exists"

**Lösung**:
```bash
git remote remove origin
git remote add origin git@gitlab.com:DEIN_USERNAME/platformio-obfuscator.git
```

### Problem: "Updates were rejected"

**Lösung**:
```bash
git pull origin main --rebase
git push -u origin main
```

---

## 📞 Fertig!

Nach erfolgreichem Push ist dein Projekt auf GitLab veröffentlicht! 🎉

**Repository-URL**: `https://gitlab.com/DEIN_USERNAME/platformio-obfuscator`

---

**Erstellt**: 2. Juni 2026  
**Projekt**: PlatformIO Project Obfuscator v2.0
