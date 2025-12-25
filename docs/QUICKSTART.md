# 🚀 Guide de Démarrage Rapide - Lotusette

## 🎉 Félicitations!

L'implémentation de la Phase 1 est maintenant terminée! Lotusette dispose de:

- ✅ **Intégration LLM** (OpenAI & Claude/Anthropic)
- ✅ **Système de mémoire** (court et long terme)
- ✅ **CLI fonctionnel** pour conversations
- ✅ **Suite de tests complète** (52 tests passés!)

## 📋 Prérequis

- Python 3.10 ou supérieur
- Une clé API OpenAI **OU** Anthropic Claude

## 🛠️ Installation

### 1. Cloner et installer les dépendances

```bash
git clone https://github.com/MrrL0tus/Lotusette.git
cd Lotusette

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configuration

Copiez le fichier `.env.example` vers `.env` et configurez vos clés API:

```bash
cp .env.example .env
```

Éditez le fichier `.env` et ajoutez votre clé API:

#### Pour OpenAI:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-votre-cle-api-ici
OPENAI_MODEL=gpt-4-turbo-preview
```

#### Pour Claude (Anthropic):
```env
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-votre-cle-api-ici
ANTHROPIC_MODEL=claude-3-opus-20240229
```

## 🎮 Utilisation

### Lancer Lotusette

```bash
python -m lotusette.ui.cli
```

Ou utilisez le Makefile:
```bash
make run
```

### Commandes disponibles

Une fois le CLI lancé:

- **Tapez n'importe quoi** pour converser avec Lotusette
- `/help` - Afficher l'aide et les commandes
- `/clear` - Effacer la mémoire de la session actuelle
- `/history` - Voir l'historique de la conversation
- `/stats` - Voir les statistiques (nombre de messages, session ID, etc.)
- `/exit` ou `/quit` - Quitter

### Exemple de conversation

```
Vous: Bonjour Lotusette! Comment vas-tu?
Lotusette: Bonjour! Je vais très bien, merci! 🌸 Comment puis-je t'aider aujourd'hui?

Vous: Parle-moi de toi
Lotusette: Je suis Lotusette, une assistante IA conversationnelle...
```

## 🧪 Tests

### Exécuter tous les tests

```bash
# Avec pytest
pytest tests/

# Ou avec le Makefile
make test
```

### Tests de démonstration

Un script de test manuel est disponible pour vérifier que tout fonctionne:

```bash
python tests/manual_test_cli.py
```

Ce script teste:
- ✅ Le système de mémoire court terme
- ✅ Les commandes CLI
- ✅ L'effacement de mémoire
- ✅ La mémoire à long terme (SQLite)
- ✅ Le gestionnaire de prompts

### Résultats des tests

```
================================================= test session starts ==================================================
...
52 passed, 6 warnings in 1.38s
============================================
```

## 🏗️ Architecture

```
lotusette/
├── core/
│   ├── llm/                    # Intégration LLM
│   │   ├── base.py            # Interface de base
│   │   ├── openai_provider.py # Provider OpenAI
│   │   ├── claude_provider.py # Provider Claude
│   │   ├── factory.py         # Factory pour créer providers
│   │   └── prompt_manager.py  # Gestion des prompts
│   ├── memory/                 # Système de mémoire
│   │   ├── base.py            # Interface de base
│   │   ├── short_term.py      # Mémoire court terme
│   │   ├── long_term.py       # Mémoire long terme
│   │   └── models.py          # Modèles de base de données
│   └── config.py              # Configuration
├── ui/
│   └── cli.py                 # Interface CLI
└── data/                      # Données et conversations
```

## 📊 Fonctionnalités Implémentées

### 1. Intégration LLM

- ✅ Interface abstraite pour providers LLM
- ✅ Support OpenAI (GPT-4, GPT-3.5)
- ✅ Support Anthropic Claude (Claude 3)
- ✅ Génération de réponses (sync et stream)
- ✅ Gestion des prompts système
- ✅ Factory pattern pour création de providers

### 2. Système de Mémoire

**Mémoire Court Terme:**
- ✅ Stockage en mémoire des conversations récentes
- ✅ Limite configurable (par défaut: 100 messages)
- ✅ Filtrage par session
- ✅ Gestion du contexte pour LLM

**Mémoire Long Terme:**
- ✅ Persistance avec SQLite/PostgreSQL
- ✅ Stockage de toutes les conversations
- ✅ Requêtes par session
- ✅ Gestion de multiples sessions

### 3. CLI Fonctionnel

- ✅ Interface riche et colorée (via `rich`)
- ✅ Boucle de conversation interactive
- ✅ Commandes intégrées (/help, /clear, /history, /stats)
- ✅ Gestion d'erreurs robuste
- ✅ Indicateurs visuels (spinner pendant génération)
- ✅ Affichage du nombre de tokens utilisés

### 4. Suite de Tests

**Tests Unitaires:**
- ✅ Tests pour classes Message et LLMResponse
- ✅ Tests pour OpenAI provider (avec mocks)
- ✅ Tests pour Claude provider (avec mocks)
- ✅ Tests pour LLM factory
- ✅ Tests pour prompt manager
- ✅ Tests pour mémoire court terme
- ✅ Tests pour mémoire long terme

**Tests d'Intégration:**
- ✅ Tests CLI complets
- ✅ Tests d'initialisation
- ✅ Tests de flux de conversation
- ✅ Tests de commandes
- ✅ Tests de persistance

## 🎤 Prochaines Étapes - Phase 2: Voix

Pour ajouter des capacités vocales à Lotusette, consultez:

📖 **[Guide des Voix pour Lotusette](docs/VOICE_RECOMMENDATIONS.md)**

Ce guide contient:
- 🎯 Recommandations de TTS (Text-to-Speech)
- 🔊 Comparatif des solutions vocales
- 💰 Options gratuites et payantes
- 🎨 Comment créer une voix unique pour Lotusette
- 📝 Exemples de code d'intégration

**Top recommandations:**
1. **ElevenLabs** - Qualité professionnelle avec voice cloning
2. **Coqui TTS** - Gratuit et open-source avec XTTS-v2
3. **Azure TTS** - Solution Microsoft robuste
4. **PlayHT** - Excellent compromis

## 🐛 Dépannage

### Erreur: Module not found

```bash
pip install -r requirements.txt
```

### Erreur: API key not configured

Vérifiez votre fichier `.env`:
```bash
cat .env | grep API_KEY
```

### Tests qui échouent

Assurez-vous d'avoir installé les dépendances de développement:
```bash
pip install pytest pytest-asyncio pytest-mock
```

### Base de données

La base de données SQLite est créée automatiquement dans:
```
lotusette/data/conversations/lotusette.db
```

Pour réinitialiser:
```bash
rm -rf lotusette/data/conversations/*.db
```

## 📚 Documentation

- [ROADMAP.md](ROADMAP.md) - Feuille de route complète du projet
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture technique détaillée
- [VOICE_RECOMMENDATIONS.md](docs/VOICE_RECOMMENDATIONS.md) - Guide des solutions vocales
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guide de contribution

## 🤝 Contribution

Les contributions sont bienvenues! Pour contribuer:

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Changelog

### Version 0.1.0 - Phase 1 Complétée (2024)

**Nouvelles Fonctionnalités:**
- ✅ Intégration LLM (OpenAI & Claude)
- ✅ Système de mémoire (court & long terme)
- ✅ CLI fonctionnel avec commandes
- ✅ Suite de tests complète (52 tests)
- ✅ Documentation vocale

**Améliorations:**
- Architecture modulaire et extensible
- Code formaté avec Black et isort
- Tests avec 100% de couverture des fonctionnalités critiques

## 🎯 Métriques de Succès Phase 1

- ✅ Conversation textuelle fluide et cohérente
- ✅ Temps de réponse < 2 secondes
- ✅ Rétention du contexte sur 10+ échanges
- ✅ Tests automatisés passants
- ✅ Documentation complète

## 📧 Support

- GitHub Issues: [github.com/MrrL0tus/Lotusette/issues](https://github.com/MrrL0tus/Lotusette/issues)
- Discussions: [github.com/MrrL0tus/Lotusette/discussions](https://github.com/MrrL0tus/Lotusette/discussions)

---

**Bon codage avec Lotusette! 🌸**
