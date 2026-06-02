#!/usr/bin/env python3
"""
PlatformIO Project Obfuscator (Enhanced Edition)
=================================================
Dieses Tool erstellt eine bereinigte Kopie eines PlatformIO-Projekts:
- Entfernt alle Kommentare aus definierten Ordnern
- Ersetzt Variablen/Funktionen durch generische Bezeichnungen
- Fügt Copyright-Header zu lib/Kaninchen Dateien hinzu
- Kopiert nur verwendete Libraries (selektiv, ohne Beispiele)
- Kompiliert das Projekt zur Verifikation

Autor: Automatisch generiert
Datum: 2026-06-02
Version: 2.0.0
"""

import os
import sys
import re
import shutil
import subprocess
import argparse
import json
from pathlib import Path
from typing import Dict, Set, List, Tuple, Optional
import hashlib
import fnmatch

# YAML Support (mit Fallback)
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class Config:
    """Konfigurations-Klasse"""
    
    DEFAULT_CONFIG = {
        'copyright_header_file': 'copyright_header.txt',
        'copyright_folders': ['src', 'lib/Kaninchen', 'include'],
        'obfuscate_extensions': ['.c', '.cpp', '.cc', '.cxx', '.h', '.hpp', '.hxx', '.ino'],
        'obfuscate_folders': ['src', 'lib/Kaninchen', 'include'],
        'obfuscation_style': 'simple',
        'obfuscation_length': 8,
        'copy_only_used_libraries': True,
        'preserve_libraries': [],
        'library_ignore_patterns': [
            'examples', 'examples/**', 'test', 'tests', 'test/**', 'tests/**',
            'docs', 'doc', 'documentation', '*.md', 'README*', 'LICENSE*',
            'CHANGELOG*', '.git', '.github', '.vscode', '*.pdf', '*.png', '*.jpg', '*.jpeg'
        ],
        'project_ignore_patterns': ['.pio', '.vscode', '.git', '__pycache__', '*.pyc', '.DS_Store'],
        'compile_after_obfuscation': True,
        'compilation_timeout': 600,
        'verbose': False,
        'mapping_file': 'obfuscation_mapping.json',
        'additional_reserved_words': [],
        'variable_prefix': 'v',
        'constant_prefix': 'C'
    }
    
    def __init__(self, config_file: Optional[Path] = None):
        self.config = self.DEFAULT_CONFIG.copy()
        
        if config_file and config_file.exists():
            self.load_config(config_file)
    
    def load_config(self, config_file: Path):
        """Lädt Konfiguration aus YAML oder JSON"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if HAS_YAML and (config_file.suffix in ['.yaml', '.yml']):
                    user_config = yaml.safe_load(f)
                else:
                    user_config = json.load(f)
            
            if user_config:
                self.config.update(user_config)
                print(f"[INFO] Konfiguration geladen: {config_file}")
        except Exception as e:
            print(f"[WARNUNG] Fehler beim Laden der Konfiguration: {e}")
            print(f"[INFO] Verwende Standard-Konfiguration")
    
    def get(self, key: str, default=None):
        """Gibt Konfigurationswert zurück"""
        return self.config.get(key, default)


class CodeObfuscator:
    """Hauptklasse für die Code-Obfuscation"""
    
    # C/C++ Keywords und Standard-Typen, die nicht umbenannt werden dürfen
    RESERVED_WORDS = {
        'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
        'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
        'inline', 'int', 'long', 'register', 'return', 'short', 'signed',
        'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned',
        'void', 'volatile', 'while', 'bool', 'true', 'false', 'nullptr',
        'class', 'namespace', 'private', 'protected', 'public', 'template',
        'this', 'virtual', 'override', 'final', 'explicit', 'operator',
        'new', 'delete', 'try', 'catch', 'throw', 'using', 'typename',
        # Arduino/ESP32 häufig genutzte Funktionen
        'pinMode', 'digitalWrite', 'digitalRead', 'analogRead', 'analogWrite',
        'delay', 'millis', 'micros', 'Serial', 'String', 'setup', 'loop',
        'begin', 'end', 'print', 'println', 'available', 'read', 'write',
        'HIGH', 'LOW', 'INPUT', 'OUTPUT', 'INPUT_PULLUP',
        # Standard-Library
        'std', 'uint8_t', 'uint16_t', 'uint32_t', 'uint64_t',
        'int8_t', 'int16_t', 'int32_t', 'int64_t', 'size_t',
        'main', 'printf', 'scanf', 'malloc', 'free', 'memcpy', 'memset'
    }
    
    def __init__(self, source_path: str, target_path: str, config: Config):
        self.source_path = Path(source_path).resolve()
        self.target_path = Path(target_path).resolve()
        self.config = config
        self.verbose = config.get('verbose', False)
        self.identifier_map: Dict[str, str] = {}
        self.identifier_counter = 0
        self.processed_files = 0
        self.mapping_file = self.target_path / config.get('mapping_file', 'obfuscation_mapping.json')
        self.copyright_header = ""
        self.used_libraries: Set[str] = set()
        
        # Erweitere RESERVED_WORDS mit zusätzlichen Wörtern aus Config
        additional_words = config.get('additional_reserved_words', [])
        if additional_words:
            self.RESERVED_WORDS = self.RESERVED_WORDS.union(set(additional_words))
        
        # Lade Copyright-Header
        self.load_copyright_header()
    
    def log(self, message: str):
        """Logging-Funktion"""
        if self.verbose:
            print(f"[INFO] {message}")
    
    def load_copyright_header(self):
        """Lädt den Copyright-Header aus Datei"""
        header_file = Path(self.config.get('copyright_header_file', 'copyright_header.txt'))
        
        # Prüfe relative und absolute Pfade
        if not header_file.is_absolute():
            # Suche relativ zum Script-Verzeichnis
            script_dir = Path(__file__).parent
            header_file = script_dir / header_file
        
        if header_file.exists():
            try:
                with open(header_file, 'r', encoding='utf-8') as f:
                    self.copyright_header = f.read()
                self.log(f"Copyright-Header geladen: {header_file}")
            except Exception as e:
                print(f"[WARNUNG] Fehler beim Laden des Copyright-Headers: {e}")
                self.copyright_header = ""
        else:
            print(f"[WARNUNG] Copyright-Header-Datei nicht gefunden: {header_file}")
            self.copyright_header = ""
    
    def should_ignore(self, path: Path, patterns: List[str]) -> bool:
        """Prüft ob ein Pfad ignoriert werden soll"""
        path_str = str(path)
        name = path.name
        
        for pattern in patterns:
            # Glob-Pattern matching
            if fnmatch.fnmatch(name, pattern):
                return True
            if fnmatch.fnmatch(path_str, f"*/{pattern}"):
                return True
            if fnmatch.fnmatch(path_str, pattern):
                return True
        
        return False
    
    def analyze_dependencies(self):
        """Analysiert welche Libraries tatsächlich verwendet werden"""
        self.log("Analysiere Library-Dependencies...")
        
        # Durchsuche src/ und lib/Kaninchen nach #include Statements
        search_dirs = [self.source_path / 'src']
        askoheat_dir = self.source_path / 'lib' / 'Kaninchen'
        if askoheat_dir.exists():
            search_dirs.append(askoheat_dir)
        
        include_pattern = re.compile(r'#include\s*[<"]([^>"]+)[>"]')
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
                
            for root, dirs, files in os.walk(search_dir):
                # Ignoriere bestimmte Verzeichnisse
                dirs[:] = [d for d in dirs if d not in {'.pio', '.git', '__pycache__'}]
                
                for file in files:
                    if Path(file).suffix in ['.c', '.cpp', '.h', '.hpp', '.ino']:
                        file_path = Path(root) / file
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                
                            # Finde alle #include Statements
                            includes = include_pattern.findall(content)
                            
                            for include in includes:
                                # Extrahiere Library-Name (erster Teil des Pfades)
                                parts = include.split('/')
                                if len(parts) > 0:
                                    lib_name = parts[0]
                                    # Prüfe ob es eine Library im lib-Ordner ist
                                    lib_path = self.source_path / 'lib' / lib_name
                                    if lib_path.exists() and lib_path.is_dir():
                                        self.used_libraries.add(lib_name)
                                        self.log(f"Gefundene Library: {lib_name} (in {file})")
                        
                        except Exception as e:
                            self.log(f"Fehler beim Analysieren von {file_path}: {e}")
        
        # Spezielle Libraries, die immer inkludiert werden sollten
        always_include = {'Kaninchen'}
        self.used_libraries.update(always_include)
        
        print(f"[INFO] Verwendete Libraries ({len(self.used_libraries)}): {', '.join(sorted(self.used_libraries))}")
    
    def copy_project_structure(self):
        """Kopiert die Projektstruktur selektiv"""
        self.log(f"Erstelle Projektstruktur: {self.target_path}")
        
        if self.target_path.exists():
            response = input(f"Zielordner {self.target_path} existiert bereits. Überschreiben? (j/n): ")
            if response.lower() != 'j':
                print("Abbruch.")
                sys.exit(0)
            shutil.rmtree(self.target_path)
        
        self.target_path.mkdir(parents=True, exist_ok=True)
        
        ignore_patterns = self.config.get('project_ignore_patterns', [])
        
        # Kopiere Root-Dateien (platformio.ini, etc.)
        for item in self.source_path.iterdir():
            if item.is_file():
                if not self.should_ignore(item, ignore_patterns):
                    shutil.copy2(item, self.target_path / item.name)
                    self.log(f"Kopiert: {item.name}")
        
        # Kopiere wichtige Ordner (src, include, etc.)
        important_dirs = ['src', 'include', 'test', 'data']
        for dir_name in important_dirs:
            src_dir = self.source_path / dir_name
            if src_dir.exists():
                dst_dir = self.target_path / dir_name
                shutil.copytree(src_dir, dst_dir, 
                              ignore=lambda d, files: [f for f in files 
                                                      if self.should_ignore(Path(d) / f, ignore_patterns)])
                self.log(f"Kopiert: {dir_name}/")
    
    def copy_libraries(self):
        """Kopiert Libraries selektiv"""
        lib_src = self.source_path / 'lib'
        lib_dst = self.target_path / 'lib'
        
        if not lib_src.exists():
            self.log("Kein lib-Ordner gefunden.")
            return
        
        lib_dst.mkdir(exist_ok=True)
        
        copy_only_used = self.config.get('copy_only_used_libraries', True)
        lib_ignore = self.config.get('library_ignore_patterns', [])
        
        for lib_dir in lib_src.iterdir():
            if not lib_dir.is_dir():
                continue
            
            lib_name = lib_dir.name
            
            # Prüfe ob Library verwendet wird
            if copy_only_used and lib_name not in self.used_libraries:
                self.log(f"Überspringe ungenutzte Library: {lib_name}")
                continue
            
            self.log(f"Kopiere Library: {lib_name}")
            
            # Kopiere Library, ignoriere bestimmte Patterns
            dst_lib = lib_dst / lib_name
            
            def ignore_func(directory, files):
                ignored = []
                for f in files:
                    file_path = Path(directory) / f
                    rel_path = file_path.relative_to(lib_src / lib_name) if file_path != lib_src / lib_name else Path(f)
                    
                    # Ignoriere nach Patterns
                    if self.should_ignore(rel_path, lib_ignore):
                        ignored.append(f)
                        self.log(f"  Ignoriere: {lib_name}/{rel_path}")
                
                return ignored
            
            shutil.copytree(lib_dir, dst_lib, ignore=ignore_func)
    
    def add_copyright_header(self, file_path: Path) -> bool:
        """Fügt Copyright-Header zu einer Datei hinzu"""
        if not self.copyright_header:
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Füge Header hinzu (mit Leerzeile danach)
            new_content = self.copyright_header + "\n" + content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
        except Exception as e:
            print(f"[FEHLER] Fehler beim Hinzufügen des Copyright-Headers zu {file_path}: {e}")
            return False
    
    def remove_comments(self, content: str) -> str:
        """Entfernt C/C++ Kommentare aus dem Code"""
        # Entfernt /* ... */ Kommentare (auch mehrzeilig)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        
        # Entfernt // Kommentare (aber nicht in Strings)
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Einfache Heuristik: Entfernt // Kommentare, wenn sie nicht in Strings sind
            in_string = False
            in_char = False
            result = []
            i = 0
            
            while i < len(line):
                # String-Literal Detection
                if line[i] == '"' and (i == 0 or line[i-1] != '\\'):
                    in_string = not in_string
                    result.append(line[i])
                # Char-Literal Detection
                elif line[i] == "'" and (i == 0 or line[i-1] != '\\'):
                    in_char = not in_char
                    result.append(line[i])
                # Comment Detection
                elif line[i:i+2] == '//' and not in_string and not in_char:
                    break  # Rest der Zeile ignorieren
                else:
                    result.append(line[i])
                i += 1
            
            cleaned_line = ''.join(result).rstrip()
            if cleaned_line:  # Nur nicht-leere Zeilen behalten
                cleaned_lines.append(cleaned_line)
        
        return '\n'.join(cleaned_lines)
    
    def generate_obfuscated_name(self, original: str) -> str:
        """Generiert einen obfuscierten Namen für einen Identifier"""
        if original in self.identifier_map:
            return self.identifier_map[original]
        
        # Prüfen ob es ein reserviertes Wort ist
        if original in self.RESERVED_WORDS:
            return original
        
        # Prüfen ob es mit einem Unterstrich beginnt (oft System-Funktionen)
        if original.startswith('_'):
            return original
        
        # Generiere Namen basierend auf Verschleierungsstil
        style = self.config.get('obfuscation_style', 'simple')
        length = self.config.get('obfuscation_length', 8)
        is_constant = original.isupper() and len(original) > 1
        
        if style == 'random':
            # Zufällige Kombination aus Buchstaben und Zahlen
            import random
            import string
            chars = string.ascii_letters + string.digits
            # Stelle sicher, dass es mit Buchstaben beginnt (gültige C-Identifikatoren)
            new_name = random.choice(string.ascii_letters) + ''.join(random.choices(chars, k=length-1))
        
        elif style == 'hex':
            # Hex-basierte Namen
            hex_val = format(self.identifier_counter, 'X').zfill(length-1)
            new_name = 'x' + hex_val
        
        elif style == 'numbered':
            # Beschreibende Präfixe mit Nummern
            prefix = 'const_' if is_constant else 'var_'
            new_name = f"{prefix}{self.identifier_counter}"
        
        else:  # 'simple' (default)
            # Einfache Präfixe
            var_prefix = self.config.get('variable_prefix', 'v')
            const_prefix = self.config.get('constant_prefix', 'C')
            prefix = const_prefix if is_constant else var_prefix
            new_name = f"{prefix}{self.identifier_counter}"
        
        self.identifier_counter += 1
        self.identifier_map[original] = new_name
        self.log(f"Mapping: {original} -> {new_name}")
        
        return new_name
    
    def find_identifiers(self, content: str) -> Set[str]:
        """Findet alle Identifikatoren im Code"""
        # Regex für C/C++ Identifikatoren
        pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
        identifiers = set(re.findall(pattern, content))
        
        # Filtert reservierte Wörter und Standardfunktionen
        identifiers = {id for id in identifiers if id not in self.RESERVED_WORDS}
        
        return identifiers
    
    def obfuscate_identifiers(self, content: str, identifiers: Set[str]) -> str:
        """Ersetzt Identifikatoren durch obfuscierte Namen"""
        # Sortiere Identifikatoren nach Länge (längste zuerst)
        # um Teilstring-Probleme zu vermeiden
        sorted_identifiers = sorted(identifiers, key=len, reverse=True)
        
        for identifier in sorted_identifiers:
            if identifier in self.RESERVED_WORDS:
                continue
            
            obfuscated = self.generate_obfuscated_name(identifier)
            
            # Word-Boundary Regex um nur ganze Wörter zu ersetzen
            pattern = r'\b' + re.escape(identifier) + r'\b'
            content = re.sub(pattern, obfuscated, content)
        
        return content
    
    def should_obfuscate_file(self, file_path: Path) -> bool:
        """Prüft ob eine Datei obfusciert werden soll"""
        # Prüfe Dateierweiterung
        if file_path.suffix not in self.config.get('obfuscate_extensions', []):
            return False
        
        # Prüfe ob Datei in einem obfuscate_folder liegt
        obfuscate_folders = self.config.get('obfuscate_folders', [])
        
        try:
            rel_path = file_path.relative_to(self.target_path)
            path_str = str(rel_path)
            
            for folder in obfuscate_folders:
                if path_str.startswith(folder.replace('\\', '/')):
                    return True
        except ValueError:
            pass
        
        return False
    
    def should_add_copyright(self, file_path: Path) -> bool:
        """Prüft ob einer Datei ein Copyright-Header hinzugefügt werden soll"""
        try:
            rel_path = file_path.relative_to(self.target_path)
            path_str = str(rel_path).replace('\\', '/')
            
            # Prüfe alle konfigurierten Copyright-Ordner
            copyright_folders = self.config.get('copyright_folders', [])
            
            for folder in copyright_folders:
                folder_normalized = folder.replace('\\', '/')
                if path_str.startswith(folder_normalized):
                    if file_path.suffix in self.config.get('obfuscate_extensions', []):
                        return True
        except ValueError:
            pass
        
        return False
    
    def process_file(self, file_path: Path) -> bool:
        """Verarbeitet eine einzelne Datei"""
        try:
            self.log(f"Verarbeite: {file_path.relative_to(self.target_path)}")
            
            # Prüfe ob Copyright-Header hinzugefügt werden soll
            if self.should_add_copyright(file_path):
                self.add_copyright_header(file_path)
                self.log(f"  Copyright-Header hinzugefügt")
            
            # Prüfe ob Datei obfusciert werden soll
            if not self.should_obfuscate_file(file_path):
                self.log(f"  Überspringe Obfuscation (preserve)")
                return True
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Schritt 1: Kommentare entfernen
            content = self.remove_comments(content)
            
            # Schritt 2: Identifikatoren finden
            identifiers = self.find_identifiers(content)
            
            # Schritt 3: Identifikatoren obfuscieren
            content = self.obfuscate_identifiers(content, identifiers)
            
            # Datei überschreiben
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.processed_files += 1
            return True
            
        except Exception as e:
            print(f"[FEHLER] Fehler beim Verarbeiten von {file_path}: {e}")
            return False
    
    def process_all_files(self):
        """Verarbeitet alle relevanten Dateien im Projekt"""
        self.log("Starte Datei-Verarbeitung...")
        
        extensions = set(self.config.get('obfuscate_extensions', []))
        
        for root, dirs, files in os.walk(self.target_path):
            # Ignoriere bestimmte Verzeichnisse
            dirs[:] = [d for d in dirs if d not in {'.pio', '.vscode', '.git', '__pycache__'}]
            
            for file in files:
                file_path = Path(root) / file
                
                # Verarbeite alle relevanten Dateien (auch die, die nicht obfusciert werden)
                if file_path.suffix in extensions:
                    self.process_file(file_path)
        
        self.log(f"Fertig! {self.processed_files} Dateien verarbeitet.")
    
    def save_mapping(self):
        """Speichert das Identifier-Mapping in eine JSON-Datei"""
        self.log(f"Speichere Mapping in {self.mapping_file}")
        
        with open(self.mapping_file, 'w', encoding='utf-8') as f:
            json.dump(self.identifier_map, f, indent=2, sort_keys=True)
        
        print(f"\n[INFO] Obfuscation-Mapping gespeichert: {self.mapping_file}")
        print(f"[INFO] Anzahl obfuscierter Identifikatoren: {len(self.identifier_map)}")
    
    def compile_project(self) -> bool:
        """Kompiliert das obfuscierte Projekt mit PlatformIO"""
        print("\n" + "="*60)
        print("KOMPILIERUNG")
        print("="*60)
        
        try:
            # Prüfe ob PlatformIO installiert ist
            result = subprocess.run(['pio', '--version'], 
                                   capture_output=True, 
                                   text=True, 
                                   timeout=10)
            
            if result.returncode != 0:
                print("[FEHLER] PlatformIO ist nicht installiert oder nicht im PATH.")
                return False
            
            self.log(f"PlatformIO Version: {result.stdout.strip()}")
            
            # Wechsle ins Zielverzeichnis und kompiliere
            print(f"\n[INFO] Kompiliere Projekt in {self.target_path}...")
            print("[INFO] Dies kann einige Minuten dauern...\n")
            
            timeout = self.config.get('compilation_timeout', 600)
            
            result = subprocess.run(['pio', 'run'], 
                                   cwd=self.target_path,
                                   capture_output=True,
                                   text=True,
                                   timeout=timeout)
            
            if result.returncode == 0:
                print("[ERFOLG] ✓ Kompilierung erfolgreich!")
                print("\n--- Build Output (letzte Zeilen) ---")
                print('\n'.join(result.stdout.split('\n')[-20:]))
                return True
            else:
                print("[FEHLER] ✗ Kompilierung fehlgeschlagen!")
                print("\n--- Error Output ---")
                print(result.stderr)
                print("\n--- Build Output ---")
                print(result.stdout)
                return False
                
        except subprocess.TimeoutExpired:
            print(f"[FEHLER] Kompilierung Timeout (>{timeout}s)")
            return False
        except FileNotFoundError:
            print("[FEHLER] 'pio' Kommando nicht gefunden. Ist PlatformIO installiert?")
            return False
        except Exception as e:
            print(f"[FEHLER] Unerwarteter Fehler bei der Kompilierung: {e}")
            return False
    
    def run(self, skip_compile: bool = False):
        """Hauptfunktion: Führt den gesamten Obfuscation-Prozess aus"""
        print("="*60)
        print("PlatformIO PROJECT OBFUSCATOR v2.0")
        print("="*60)
        print(f"Source: {self.source_path}")
        print(f"Target: {self.target_path}")
        print(f"Config: {'Loaded' if self.config else 'Default'}")
        print("="*60 + "\n")
        
        # Schritt 1: Dependencies analysieren
        if self.config.get('copy_only_used_libraries', False):
            self.analyze_dependencies()
        
        # Schritt 2: Projekt kopieren
        self.copy_project_structure()
        
        # Schritt 3: Libraries kopieren
        self.copy_libraries()
        
        # Schritt 4: Dateien verarbeiten
        self.process_all_files()
        
        # Schritt 5: Mapping speichern
        self.save_mapping()
        
        # Schritt 6: Kompilieren
        compile_success = True
        if not skip_compile and self.config.get('compile_after_obfuscation', True):
            compile_success = self.compile_project()
        
        print("\n" + "="*60)
        print("ZUSAMMENFASSUNG")
        print("="*60)
        print(f"Verarbeitete Dateien: {self.processed_files}")
        print(f"Obfuscierte Identifikatoren: {len(self.identifier_map)}")
        print(f"Verwendete Libraries: {len(self.used_libraries)}")
        if not skip_compile and self.config.get('compile_after_obfuscation', True):
            print(f"Kompilierung: {'✓ ERFOLGREICH' if compile_success else '✗ FEHLGESCHLAGEN'}")
        print(f"Obfusciertes Projekt: {self.target_path}")
        print("="*60 + "\n")
        
        if not compile_success and not skip_compile:
            print("[WARNUNG] Die Kompilierung ist fehlgeschlagen.")
            print("[HINWEIS] Das obfuscierte Projekt könnte Fehler enthalten.")
            print("[TIPP] Prüfe die Compiler-Fehler und passe ggf. RESERVED_WORDS an.")


def main():
    """Haupteinstiegspunkt"""
    parser = argparse.ArgumentParser(
        description='PlatformIO Project Obfuscator v2.0 - Entfernt Kommentare, obfusciert Code, fügt Copyright hinzu',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  %(prog)s /path/to/source /path/to/target
  %(prog)s /path/to/source /path/to/target --config config.yaml
  %(prog)s /path/to/source /path/to/target --verbose
  %(prog)s /path/to/source /path/to/target --skip-compile
        """
    )
    
    parser.add_argument('source', 
                       help='Quellpfad des PlatformIO-Projekts')
    parser.add_argument('target', 
                       help='Zielpfad für das obfuscierte Projekt')
    parser.add_argument('-c', '--config',
                       help='Pfad zur Konfigurationsdatei (YAML oder JSON)',
                       default=None)
    parser.add_argument('-v', '--verbose', 
                       action='store_true',
                       help='Ausführliche Ausgabe')
    parser.add_argument('-s', '--skip-compile',
                       action='store_true',
                       help='Kompilierung überspringen')
    
    args = parser.parse_args()
    
    # Validierung
    source = Path(args.source)
    if not source.exists():
        print(f"[FEHLER] Quellpfad existiert nicht: {source}")
        sys.exit(1)
    
    if not (source / 'platformio.ini').exists():
        print(f"[FEHLER] Kein PlatformIO-Projekt gefunden (platformio.ini fehlt)")
        sys.exit(1)
    
    # Lade Konfiguration
    config_file = None
    if args.config:
        config_file = Path(args.config)
        if not config_file.exists():
            print(f"[FEHLER] Konfigurationsdatei nicht gefunden: {config_file}")
            sys.exit(1)
    else:
        # Suche nach config.yaml im aktuellen Verzeichnis
        for name in ['config.yaml', 'config.yml', 'config.json']:
            candidate = Path(name)
            if candidate.exists():
                config_file = candidate
                break
    
    config = Config(config_file)
    
    # Override verbose aus Commandline
    if args.verbose:
        config.config['verbose'] = True
    
    # Obfuscator ausführen
    obfuscator = CodeObfuscator(args.source, args.target, config)
    
    try:
        obfuscator.run(skip_compile=args.skip_compile)
    except KeyboardInterrupt:
        print("\n\n[ABBRUCH] Durch Benutzer unterbrochen.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FEHLER] Unerwarteter Fehler: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
