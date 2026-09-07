# Quick Start Guide - Lotusette

Ce guide vous aidera à démarrer rapidement avec Lotusette.

## Prérequis

- Python 3.10 ou supérieur
- Git
- (Optionnel) Compte OpenAI ou Anthropic pour l'API LLM

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/MrrL0tus/Lotusette.git
cd Lotusette
```

### 2. Créer un environnement virtuel

**Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Installer les dépendances

**Installation de base:**
```bash
pip install -r requirements.txt
```

**Installation pour le développement:**
```bash
pip install -r requirements-dev.txt
```

### 4. Configuration

Copier le fichier d'exemple de configuration:
```bash
cp .env.example .env
```

Éditer `.env` et ajouter vos clés API:
```bash
# Exemple de configuration minimale
OPENAI_API_KEY=sk-your-key-here
LLM_PROVIDER=openai
```

## Utilisation

### Interface CLI

Lancer l'interface en ligne de commande:

```bash
python -m lotusette.ui.cli
```

Ou avec make:
```bash
make run
```

### Tests

Lancer les tests:
```bash
# Tous les tests
pytest

# Tests avec couverture
make test

# Tests verbeux
make test-verbose
```

### Développement

Format du code:
```bash
make format
```

Vérification du code:
```bash
make lint
```

## Structure du Projet

```
Lotusette/
├── lotusette/          # Code source principal
│   ├── core/          # Fonctionnalités principales
│   ├── voice/         # Capacités vocales (futur)
│   ├── web/           # Accès web (futur)
│   ├── gaming/        # Gaming (futur)
│   ├── api/           # API REST (futur)
│   └── ui/            # Interfaces utilisateur
├── tests/             # Tests
├── docs/              # Documentation
├── .env.example       # Exemple de configuration
├── requirements.txt   # Dépendances
└── README.md          # Ce fichier
```

## Prochaines Étapes

1. **Consultez la Roadmap**: Lisez [ROADMAP.md](../ROADMAP.md) pour comprendre la vision du projet
2. **Architecture**: Explorez [ARCHITECTURE.md](../ARCHITECTURE.md) pour les détails techniques
3. **Contribuer**: Voir [CONTRIBUTING.md](../CONTRIBUTING.md) pour contribuer au projet

## Dépannage

### Problèmes d'installation

**Erreur: command 'gcc' not found**
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# macOS
xcode-select --install
```

**Erreur lors de l'installation de PyAudio**
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev

# macOS
brew install portaudio
```

### Problèmes de configuration

**Erreur: OPENAI_API_KEY not found**
- Vérifiez que le fichier `.env` existe et contient votre clé API
- Assurez-vous que la clé est valide

### Obtenir de l'aide

- 📝 Ouvrez une [issue sur GitHub](https://github.com/MrrL0tus/Lotusette/issues)
- 💬 Consultez les [GitHub Discussions](https://github.com/MrrL0tus/Lotusette/discussions)

## Ressources

- [Documentation complète](./README.md)
- [Roadmap du projet](../ROADMAP.md)
- [Architecture technique](../ARCHITECTURE.md)
- [Guide de contribution](../CONTRIBUTING.md)

---

Bon développement avec Lotusette! 🌸
