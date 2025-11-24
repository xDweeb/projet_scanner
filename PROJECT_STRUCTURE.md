# 🛡️ Cyber Scanner PRO - Structure du Projet

## 📁 Architecture du Projet

```
projet_scanner/
├── 📄 main.py                     # Point d'entrée principal
├── 📄 start_scanner.bat           # Lanceur Windows
├── 📄 requirements.txt            # Dépendances Python
├── 📄 README.md                   # Documentation principale
│
├── 📂 src/                        # Code source principal
│   ├── 📂 core/                   # Moteur de scan
│   │   ├── 📄 scanner_engine.py   # Fonctions de scan réseau
│   │   └── 📄 __init__.py         # Module init
│   │
│   ├── 📂 gui/                    # Interface utilisateur
│   │   ├── 📄 main_window.py      # Fenêtre principale moderne
│   │   └── 📄 __init__.py         # Module init
│   │
│   ├── 📂 database/               # Gestion base de données
│   │   ├── 📄 db_manager.py       # Gestionnaire SQLite
│   │   └── 📄 __init__.py         # Module init
│   │
│   └── 📂 utils/                  # Utilitaires
│       ├── 📄 themes.py           # Gestion des thèmes
│       ├── 📄 validators.py       # Validation des entrées
│       └── 📄 __init__.py         # Module init
│
├── 📂 assets/                     # Ressources graphiques
│   ├── 🖼️ logo.png               # Logo principal
│   ├── 🖼️ icons/                 # Icônes diverses
│   └── 🖼️ screenshots/           # Captures d'écran
│
├── 📂 output/                     # Fichiers de sortie
│   ├── 📄 scan_history.db        # Base de données des scans
│   ├── 📄 scan_results.txt       # Résultats par défaut
│   └── 📂 exports/               # Exports personnalisés
│
├── 📂 docs/                       # Documentation
│   ├── 📄 installation.md        # Guide d'installation
│   ├── 📄 user_guide.md          # Guide utilisateur
│   ├── 📄 api_reference.md       # Référence API
│   └── 📄 changelog.md           # Historique des versions
│
├── 📂 legacy/                     # Anciennes versions
│   ├── 📄 scanner_gui_modern.py  # Ancienne GUI moderne
│   ├── 📄 scanner_gui_pro.py     # Version pro précédente
│   ├── 📄 scanner_functions.py   # Anciennes fonctions
│   └── 📄 database.py            # Ancien gestionnaire DB
│
└── 📂 tests/                      # Tests unitaires
    ├── 📄 test_scanner.py        # Tests du moteur de scan
    ├── 📄 test_database.py       # Tests de la base de données
    └── 📄 __init__.py            # Module init
```

## 🚀 Utilisation

### Démarrage rapide
```bash
# Méthode 1: Lanceur automatique
python main.py

# Méthode 2: Batch Windows
start_scanner.bat

# Méthode 3: Direct GUI
python src/gui/main_window.py
```

### Installation des dépendances
```bash
pip install -r requirements.txt
```

## 🔧 Modules Principaux

### 1. **scanner_engine.py** - Moteur de Scan
- `port_scan()` - Scan de ports TCP
- `ip_lookup()` - Géolocalisation IP
- `whois_lookup()` - Informations WHOIS
- `ping_host()` - Test de connectivité
- `get_my_ip()` - IP publique
- `wifi_scan()` - Réseaux WiFi

### 2. **db_manager.py** - Base de Données
- `ScanDatabase` - Gestionnaire SQLite
- Historique des scans
- Paramètres utilisateur
- Statistiques

### 3. **main_window.py** - Interface Graphique
- Interface moderne dark/light
- Écran de démarrage avec logo
- Vérification d'âge
- Fonctionnalités complètes

## 📊 Fonctionnalités

### ✅ Scans Disponibles
- 🔍 **Port Scanning** - Scan TCP avec détection de services
- 🌐 **Network Discovery** - Découverte d'hôtes actifs
- 📡 **Ping Test** - Test de connectivité réseau
- 🌍 **IP Lookup** - Géolocalisation et informations ISP
- 📋 **WHOIS Lookup** - Informations domaine/registrar
- 💻 **System Info** - Informations système locales

### 🎨 Interface
- 🌙 **Thème sombre/clair** - Basculement dynamique
- 🛡️ **Écran de démarrage** - Logo animé 3 secondes
- 🔒 **Vérification d'âge** - Accès 18+ requis
- ⏹️ **Contrôle de scan** - Stop, pause, export
- 📊 **Historique** - Base de données SQLite

### ⚙️ Configuration
- 🚀 **Vitesses de scan** - Rapide/Normal/Lent/Très lent
- 💾 **Sauvegarde auto** - Résultats dans output/
- 🎯 **Détection de services** - Identification ports communs
- 📈 **Statistiques** - Compteurs et historique

## 📝 Versions

### Version 2.0 (Actuelle)
- ✅ Architecture modulaire organisée
- ✅ Interface moderne complète
- ✅ Base de données SQLite
- ✅ Thèmes dark/light
- ✅ WHOIS lookup intégré
- ✅ Export et historique

### Version 1.x (Legacy)
- Interface basique
- Fonctions simples
- Fichiers uniques

## 🔒 Sécurité

- Vérification d'âge obligatoire (18+)
- Validation des entrées utilisateur
- Timeouts de sécurité pour les scans
- Gestion d'erreurs robuste
- Logs des activités

## 🤝 Contribution

Pour contribuer au projet:
1. Fork le repository
2. Créer une branche feature
3. Suivre l'architecture modulaire
4. Tester les modifications
5. Soumettre une pull request

## 📄 License

Usage éducatif et professionnel uniquement.
Utilisation responsable requise.
