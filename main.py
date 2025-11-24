#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cyber Scanner PRO - Main Launcher
Professional Network Security Scanner

Author: xdweb
Version: 2.0
Date: November 2024
"""

import sys
import os
import subprocess
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        ("requests", "requests"),
        ("PIL", "Pillow"), 
        ("whois", "python-whois"),
        ("tkinter", "tkinter (built-in)")
    ]
    
    missing_packages = []
    
    print("🔍 Vérification des modules requis...")
    
    for module_name, package_name in required_packages:
        try:
            if module_name == "PIL":
                import PIL
            elif module_name == "tkinter":
                import tkinter
            else:
                __import__(module_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - MANQUANT")
            if package_name != "tkinter (built-in)":
                missing_packages.append(package_name)
    
    return missing_packages

def install_dependencies(packages):
    """Install missing dependencies"""
    if not packages:
        return True
    
    print(f"\n📦 Installation des paquets manquants: {', '.join(packages)}")
    
    try:
        # Install packages
        for package in packages:
            print(f"Installation de {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print("✅ Toutes les dépendances ont été installées avec succès!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def create_project_structure():
    """Create necessary project directories"""
    directories = [
        "output",
        "assets", 
        "logs",
        "exports"
    ]
    
    for directory in directories:
        dir_path = project_root / directory
        dir_path.mkdir(exist_ok=True)

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🛡️  CYBER SCANNER PRO - LANCEUR v2.0")
    print("=" * 60)
    print(f"📁 Répertoire de travail: {project_root}")
    
    # Create project structure
    create_project_structure()
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"\n⚠️  Modules manquants détectés: {len(missing)}")
        response = input("Voulez-vous les installer automatiquement? (o/n): ").lower()
        
        if response in ['o', 'oui', 'y', 'yes']:
            if not install_dependencies(missing):
                print("\n❌ Échec de l'installation automatique. Veuillez installer manuellement:")
                print("pip install -r requirements.txt")
                input("Appuyez sur Entrée pour quitter...")
                return
        else:
            print("\n⚠️  Veuillez installer les modules requis manuellement:")
            print("pip install -r requirements.txt")
            input("Appuyez sur Entrée pour quitter...")
            return
    
    # Lancer l'application
    print("\n🚀 Démarrage de Cyber Scanner PRO...")
    print("=" * 60)
    
    try:
        # Import and run the GUI
        from src.gui.main_window import CyberScannerPRO
        app = CyberScannerPRO()
        
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("Vérifiez que tous les fichiers sont présents dans src/")
        input("Appuyez sur Entrée pour quitter...")
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Application interrompue par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur fatale: {e}")
        input("Appuyez sur Entrée pour quitter...")
