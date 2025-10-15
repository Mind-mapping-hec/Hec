#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mind Map Mini - Installation et Configuration Complète
Script tout-en-un pour installer, configurer et lancer Mind Map Mini
"""

import os
import sys
import subprocess
import platform
import shutil
import json
import webbrowser
import time
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
VERSION = "1.0.0"
DEFAULT_PORT = 5000
DEFAULT_LANG = "fr"

# Messages multilingues
MESSAGES = {
    'fr': {
        'welcome': """
╔══════════════════════════════════════════╗
║     🧠 Mind Map Mini - Installation      ║
║    Outil de Cartographie Mentale v{}   ║
║         Interface Française              ║
╚══════════════════════════════════════════╝
        """,
        'checking_python': "🔍 Vérification de Python...",
        'python_ok': "✅ Python {} détecté",
        'python_error': "❌ Python 3.7+ requis (version actuelle: {})",
        'creating_dirs': "📁 Création des dossiers...",
        'dir_created': "   ✅ {}",
        'installing_deps': "📦 Installation des dépendances...",
        'deps_installed': "✅ Dépendances installées",
        'creating_files': "📝 Création des fichiers...",
        'file_created': "   ✅ {}",
        'setup_complete': "✨ Installation terminée !",
        'starting_server': "🚀 Démarrage du serveur...",
        'server_running': "📱 Serveur actif sur http://localhost:{}",
        'opening_browser': "🌐 Ouverture du navigateur...",
        'press_ctrl_c': "Appuyez sur Ctrl+C pour arrêter le serveur",
        'backup_created': "💾 Sauvegarde créée : {}",
        'restore_complete': "✅ Restauration terminée",
        'maps_found': "📊 {} carte(s) trouvée(s)",
        'export_complete': "📤 Export terminé : {}",
        'cleanup_complete': "🧹 Nettoyage terminé",
        'error': "❌ Erreur : {}",
        'choose_action': """
Que souhaitez-vous faire ?

1. 🚀 Installation complète
2. 📦 Installer uniquement les dépendances
3. 💾 Sauvegarder toutes les cartes
4. 📥 Restaurer une sauvegarde
5. 🧹 Nettoyer les fichiers temporaires
6. 📊 Afficher les statistiques
7. 🔧 Vérifier l'installation
8. ❓ Aide
9. 🚪 Quitter

Votre choix : """
    },
    'en': {
        'welcome': """
╔══════════════════════════════════════════╗
║     🧠 Mind Map Mini - Installation      ║
║      Mind Mapping Tool v{}             ║
║          English Interface               ║
╚══════════════════════════════════════════╝
        """,
        'checking_python': "🔍 Checking Python...",
        'python_ok': "✅ Python {} detected",
        'python_error': "❌ Python 3.7+ required (current: {})",
        'creating_dirs': "📁 Creating directories...",
        'dir_created': "   ✅ {}",
        'installing_deps': "📦 Installing dependencies...",
        'deps_installed': "✅ Dependencies installed",
        'creating_files': "📝 Creating files...",
        'file_created': "   ✅ {}",
        'setup_complete': "✨ Setup complete!",
        'starting_server': "🚀 Starting server...",
        'server_running': "📱 Server running on http://localhost:{}",
        'opening_browser': "🌐 Opening browser...",
        'press_ctrl_c': "Press Ctrl+C to stop the server",
        'backup_created': "💾 Backup created: {}",
        'restore_complete': "✅ Restore complete",
        'maps_found': "📊 {} map(s) found",
        'export_complete': "📤 Export complete: {}",
        'cleanup_complete': "🧹 Cleanup complete",
        'error': "❌ Error: {}",
        'choose_action': """
What would you like to do?

1. 🚀 Complete installation
2. 📦 Install dependencies only
3. 💾 Backup all maps
4. 📥 Restore backup
5. 🧹 Clean temporary files
6. 📊 Show statistics
7. 🔧 Verify installation
8. ❓ Help
9. 🚪 Quit

Your choice: """
    }
}

class MindMapMiniInstaller:
    """Installateur et gestionnaire pour Mind Map Mini"""
    
    def __init__(self, language='fr'):
        self.language = language
        self.msg = MESSAGES[language]
        self.base_dir = Path.cwd()
        self.venv_dir = self.base_dir / 'venv'
        
        # Dossiers requis
        self.required_dirs = [
            'mindmaps',
            'map_templates',
            'exports',
            'autosave',
            'backups',
            'static',
            'templates'
        ]
    
    def print_message(self, key, *args):
        """Afficher un message traduit"""
        message = self.msg.get(key, key)
        if args:
            message = message.format(*args)
        print(message)
    
    def check_python_version(self):
        """Vérifier la version de Python"""
        self.print_message('checking_python')
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        if version.major < 3 or (version.major == 3 and version.minor < 7):
            self.print_message('python_error', version_str)
            return False
        
        self.print_message('python_ok', version_str)
        return True
    
    def create_directories(self):
        """Créer la structure de dossiers"""
        self.print_message('creating_dirs')
        
        for dir_name in self.required_dirs:
            dir_path = self.base_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            self.print_message('dir_created', dir_name)
            
            # Créer .gitkeep pour les dossiers vides
            gitkeep = dir_path / '.gitkeep'
            gitkeep.touch()
    
    def install_dependencies(self):
        """Installer les dépendances Python"""
        self.print_message('installing_deps')
        
        requirements = [
            'Flask==2.3.3',
            'flask-cors==4.0.0'
        ]
        
        try:
            # Créer un environnement virtuel si demandé
            if not self.venv_dir.exists():
                response = input("\n🐍 Créer un environnement virtuel ? (o/n) : ")
                if response.lower() in ['o', 'y', 'oui', 'yes']:
                    subprocess.run([sys.executable, '-m', 'venv', str(self.venv_dir)])
                    print(f"   ✅ Environnement virtuel créé dans {self.venv_dir}")
            
            # Installer les packages
            for package in requirements:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                             capture_output=True, text=True)
            
            self.print_message('deps_installed')
            return True
            
        except Exception as e:
            self.print_message('error', str(e))
            return False
    
    def create_config_files(self):
        """Créer les fichiers de configuration"""
        self.print_message('creating_files')
        
        # requirements.txt
        requirements_content = """# Mind Map Mini - Requirements
Flask==2.3.3
flask-cors==4.0.0
"""
        with open('requirements.txt', 'w') as f:
            f.write(requirements_content)
        self.print_message('file_created', 'requirements.txt')
        
        # .env (configuration)
        env_content = f"""# Mind Map Mini Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=mindmap-mini-secret-{datetime.now().strftime('%Y%m%d')}
DEFAULT_LANGUAGE={DEFAULT_LANG}
DEFAULT_PORT={DEFAULT_PORT}
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        self.print_message('file_created', '.env')
        
        # .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Mind Map Mini
mindmaps/*.json
autosave/*.json
backups/*.json
exports/*
!map_templates/*.json

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# Env
.env
.env.local
"""
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        self.print_message('file_created', '.gitignore')
        
        # README.md
        readme_content = f"""# 🧠 Mind Map Mini

Version {VERSION} - Outil de cartographie mentale léger et portable

## Installation Rapide

```bash
python installer.py
```

## Utilisation

```bash
python app.py
```

Puis ouvrir http://localhost:{DEFAULT_PORT}

## Caractéristiques

- 🇫🇷 Interface bilingue (Français/English)
- 🧠 Méthode GRINDE pour l'apprentissage
- 💾 Sauvegarde automatique en JSON
- 🔒 100% privé et hors ligne
- 📤 Export en multiple formats

## Structure

```
mindmap-mini/
├── app.py              # Application Flask
├── templates/
│   └── index.html     # Interface web
├── mindmaps/          # Vos cartes mentales
├── map_templates/     # Modèles prédéfinis
└── autosave/         # Sauvegardes automatiques
```

## Support

Documentation complète dans le dossier `docs/`

---

Mind Map Mini - La cartographie mentale simple et efficace
"""
        with open('README.md', 'w') as f:
            f.write(readme_content)
        self.print_message('file_created', 'README.md')
    
    def create_launch_scripts(self):
        """Créer les scripts de lancement pour différents OS"""
        system = platform.system()
        
        if system == 'Windows':
            # Script batch pour Windows
            batch_content = f"""@echo off
echo Starting Mind Map Mini...
python app.py
pause
"""
            with open('start.bat', 'w') as f:
                f.write(batch_content)
            self.print_message('file_created', 'start.bat')
            
        else:
            # Script shell pour Unix/Linux/Mac
            shell_content = f"""#!/bin/bash
echo "🧠 Starting Mind Map Mini..."
python3 app.py
"""
            with open('start.sh', 'w') as f:
                f.write(shell_content)
            os.chmod('start.sh', 0o755)
            self.print_message('file_created', 'start.sh')
    
    def backup_maps(self):
        """Sauvegarder toutes les cartes"""
        backup_dir = self.base_dir / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = backup_dir / f'backup_{timestamp}.json'
        
        maps_dir = self.base_dir / 'mindmaps'
        all_maps = []
        
        if maps_dir.exists():
            for map_file in maps_dir.glob('*.json'):
                try:
                    with open(map_file, 'r', encoding='utf-8') as f:
                        map_data = json.load(f)
                        all_maps.append(map_data)
                except:
                    continue
        
        backup_data = {
            'version': VERSION,
            'timestamp': timestamp,
            'maps_count': len(all_maps),
            'maps': all_maps
        }
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        self.print_message('backup_created', backup_file.name)
        self.print_message('maps_found', len(all_maps))
    
    def restore_backup(self, backup_file=None):
        """Restaurer une sauvegarde"""
        backup_dir = self.base_dir / 'backups'
        
        if not backup_file:
            # Lister les sauvegardes disponibles
            backups = list(backup_dir.glob('backup_*.json'))
            if not backups:
                print("Aucune sauvegarde trouvée")
                return
            
            print("\nSauvegardes disponibles :")
            for i, backup in enumerate(backups, 1):
                print(f"{i}. {backup.name}")
            
            choice = input("\nChoisir le numéro de la sauvegarde : ")
            try:
                backup_file = backups[int(choice) - 1]
            except:
                self.print_message('error', "Choix invalide")
                return
        
        # Restaurer
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            maps_dir = self.base_dir / 'mindmaps'
            maps_dir.mkdir(exist_ok=True)
            
            for map_data in backup_data.get('maps', []):
                map_id = map_data.get('id', f"restored_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
                map_file = maps_dir / f"{map_id}.json"
                
                with open(map_file, 'w', encoding='utf-8') as f:
                    json.dump(map_data, f, indent=2, ensure_ascii=False)
            
            self.print_message('restore_complete')
            self.print_message('maps_found', len(backup_data.get('maps', [])))
            
        except Exception as e:
            self.print_message('error', str(e))
    
    def cleanup(self):
        """Nettoyer les fichiers temporaires"""
        self.print_message('cleanup_complete')
        
        # Nettoyer autosave
        autosave_dir = self.base_dir / 'autosave'
        if autosave_dir.exists():
            for file in autosave_dir.glob('*'):
                if file.name != '.gitkeep':
                    file.unlink()
        
        # Nettoyer les vieux backups (garder les 10 derniers)
        backup_dir = self.base_dir / 'backups'
        if backup_dir.exists():
            backups = sorted(backup_dir.glob('backup_*.json'))
            for backup in backups[:-10]:
                backup.unlink()
    
    def show_statistics(self):
        """Afficher les statistiques"""
        maps_dir = self.base_dir / 'mindmaps'
        
        if not maps_dir.exists():
            print("Aucune carte trouvée")
            return
        
        total_maps = 0
        total_nodes = 0
        total_connections = 0
        modes = {'grinde': 0, 'buzan': 0}
        
        for map_file in maps_dir.glob('*.json'):
            try:
                with open(map_file, 'r', encoding='utf-8') as f:
                    map_data = json.load(f)
                    total_maps += 1
                    total_nodes += len(map_data.get('nodes', []))
                    total_connections += len(map_data.get('connections', []))
                    mode = map_data.get('mode', 'grinde')
                    modes[mode] = modes.get(mode, 0) + 1
            except:
                continue
        
        print(f"""
📊 Statistiques Mind Map Mini
{'='*40}
📁 Total des cartes : {total_maps}
🔵 Total des nœuds : {total_nodes}
🔗 Total des connexions : {total_connections}
🧠 Mode GRINDE : {modes.get('grinde', 0)} cartes
🌟 Mode Buzan : {modes.get('buzan', 0)} cartes
📊 Moyenne nœuds/carte : {total_nodes/total_maps if total_maps else 0:.1f}
📈 Moyenne connexions/carte : {total_connections/total_maps if total_maps else 0:.1f}
        """)
    
    def verify_installation(self):
        """Vérifier l'installation"""
        print("\n🔧 Vérification de l'installation...")
        
        checks = {
            'Python 3.7+': self.check_python_version(),
            'Flask installé': self.check_package('flask'),
            'Flask-CORS installé': self.check_package('flask-cors'),
            'Dossier mindmaps': (self.base_dir / 'mindmaps').exists(),
            'Dossier templates': (self.base_dir / 'templates').exists(),
            'app.py présent': (self.base_dir / 'app.py').exists(),
            'index.html présent': (self.base_dir / 'templates' / 'index.html').exists()
        }
        
        all_ok = True
        for check, status in checks.items():
            symbol = "✅" if status else "❌"
            print(f"{symbol} {check}")
            if not status:
                all_ok = False
        
        if all_ok:
            print("\n✨ Installation complète et fonctionnelle !")
        else:
            print("\n⚠️ Des éléments manquent. Lancez l'installation complète.")
        
        return all_ok
    
    def check_package(self, package_name):
        """Vérifier si un package Python est installé"""
        try:
            __import__(package_name.replace('-', '_'))
            return True
        except ImportError:
            return False
    
    def complete_installation(self):
        """Installation complète"""
        print(self.msg['welcome'].format(VERSION))
        
        # Vérifier Python
        if not self.check_python_version():
            return False
        
        # Créer les dossiers
        self.create_directories()
        
        # Installer les dépendances
        self.install_dependencies()
        
        # Créer les fichiers de config
        self.create_config_files()
        
        # Créer les scripts de lancement
        self.create_launch_scripts()
        
        self.print_message('setup_complete')
        
        # Proposer de lancer le serveur
        response = input("\n🚀 Lancer Mind Map Mini maintenant ? (o/n) : ")
        if response.lower() in ['o', 'y', 'oui', 'yes']:
            self.launch_server()
        
        return True
    
    def launch_server(self):
        """Lancer le serveur Flask"""
        self.print_message('starting_server')
        
        # Vérifier que les fichiers nécessaires existent
        if not (self.base_dir / 'app.py').exists():
            self.print_message('error', "app.py manquant")
            print("Créez app.py avec le code Flask de l'artifact")
            return
        
        if not (self.base_dir / 'templates' / 'index.html').exists():
            self.print_message('error', "templates/index.html manquant")
            print("Créez templates/index.html avec le code HTML de l'artifact")
            return
        
        # Ouvrir le navigateur après un délai
        import threading
        def open_browser():
            time.sleep(3)
            webbrowser.open(f'http://localhost:{DEFAULT_PORT}')
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        self.print_message('opening_browser')
        self.print_message('server_running', DEFAULT_PORT)
        self.print_message('press_ctrl_c')
        
        # Lancer Flask
        try:
            subprocess.run([sys.executable, 'app.py'])
        except KeyboardInterrupt:
            print("\n\n👋 Mind Map Mini arrêté. À bientôt !")
    
    def show_help(self):
        """Afficher l'aide"""
        help_text = f"""
{'='*60}
🧠 MIND MAP MINI - AIDE
{'='*60}

VERSION : {VERSION}
LANGUE : {self.language.upper()}

COMMANDES DISPONIBLES :
----------------------
1. Installation complète
   - Vérifie Python
   - Crée les dossiers
   - Installe Flask
   - Configure l'application

2. Installation des dépendances
   - Installe Flask et flask-cors uniquement

3. Sauvegarde
   - Crée une sauvegarde de toutes vos cartes
   - Stockée dans backups/

4. Restauration
   - Restaure une sauvegarde précédente

5. Nettoyage
   - Supprime les fichiers temporaires
   - Garde les 10 dernières sauvegardes

6. Statistiques
   - Affiche les stats de vos cartes

7. Vérification
   - Vérifie l'installation

UTILISATION :
------------
Après installation :
1. Lancer : python app.py
2. Ouvrir : http://localhost:{DEFAULT_PORT}
3. Créer vos cartes mentales !

RACCOURCIS :
-----------
• Double-clic : Nouveau nœud
• Shift+Glisser : Naviguer
• Ctrl+S : Sauvegarder
• Delete : Supprimer nœud

MÉTHODES :
---------
• GRINDE : Optimisé apprentissage
• Buzan : Classique créatif

SUPPORT :
--------
📧 support@mindmapmini.fr
📚 Documentation dans docs/
🐛 Issues sur GitHub

{'='*60}
        """
        print(help_text)
    
    def interactive_menu(self):
        """Menu interactif"""
        while True:
            print(self.msg['choose_action'])
            choice = input().strip()
            
            if choice == '1':
                self.complete_installation()
            elif choice == '2':
                self.install_dependencies()
            elif choice == '3':
                self.backup_maps()
            elif choice == '4':
                self.restore_backup()
            elif choice == '5':
                self.cleanup()
            elif choice == '6':
                self.show_statistics()
            elif choice == '7':
                self.verify_installation()
            elif choice == '8':
                self.show_help()
            elif choice == '9':
                print("\n👋 Au revoir !")
                break
            else:
                print("Choix invalide")
            
            input("\nAppuyez sur Entrée pour continuer...")

def main():
    """Point d'entrée principal"""
    parser = argparse.ArgumentParser(description='Mind Map Mini - Installer')
    parser.add_argument('--lang', choices=['fr', 'en'], default='fr',
                       help='Language (fr or en)')
    parser.add_argument('--install', action='store_true',
                       help='Run complete installation')
    parser.add_argument('--launch', action='store_true',
                       help='Launch server')
    parser.add_argument('--backup', action='store_true',
                       help='Backup all maps')
    parser.add_argument('--stats', action='store_true',
                       help='Show statistics')
    parser.add_argument('--verify', action='store_true',
                       help='Verify installation')
    
    args = parser.parse_args()
    
    installer = MindMapMiniInstaller(language=args.lang)
    
    if args.install:
        installer.complete_installation()
    elif args.launch:
        installer.launch_server()
    elif args.backup:
        installer.backup_maps()
    elif args.stats:
        installer.show_statistics()
    elif args.verify:
        installer.verify_installation()
    else:
        # Mode interactif
        installer.interactive_menu()

if __name__ == '__main__':
    main()