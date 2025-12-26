# Lotusette

**Une IA conversationnelle évolutive inspirée de Neuro-sama**

## 📋 Vue d'ensemble

Lotusette est un projet ambitieux visant à créer un assistant IA capable de:
- 💬 **Converser naturellement** par texte et voix
- 🧠 **Apprendre et évoluer** à partir des interactions
- 🌐 **Accéder à Internet** pour fournir une assistance complète
- 🎮 **Jouer à des jeux** et apprendre de nouvelles compétences
- 🤖 **S'intégrer à un robot** pour une interaction physique (future)

## 🗺️ Roadmap

Consultez [ROADMAP.md](ROADMAP.md) pour la feuille de route complète du projet, organisée en 6 phases:

1. **Phase 1**: Fondations de base (0-3 mois)
2. **Phase 2**: Capacités vocales (3-6 mois)
3. **Phase 3**: Apprentissage et évolution (6-9 mois)
4. **Phase 4**: Accès Internet et assistance (9-12 mois)
5. **Phase 5**: Gaming et interactivité (12-18 mois)
6. **Phase 6**: Robotique et incarnation (18-24 mois)

## 🏗️ Architecture

```
lotusette/
├── core/               # Moteur principal (LLM, mémoire, personnalité)
├── voice/             # Capacités vocales (STT, TTS)
├── web/               # Accès internet et outils
├── gaming/            # Capacités de jeu et RL
├── robotics/          # Interface robotique (futur)
├── api/               # API REST/WebSocket
├── ui/                # Interfaces utilisateur
├── data/              # Données et modèles
└── tests/             # Tests
```

## 🚀 Démarrage rapide

### Prérequis
- Python 3.10 ou 3.11 (⚠️ **Python 3.13 n'est pas supporté** - voir solution Docker ci-dessous)
- pip ou poetry pour la gestion des dépendances
- (Optionnel) GPU pour les modèles locaux

### ⚠️ Problème avec Python 3.13 ?

Si vous avez Python 3.13, utilisez Docker pour garantir la compatibilité:

```bash
# Installation avec Docker (recommandé)
git clone https://github.com/MrrL0tus/Lotusette.git
cd Lotusette
chmod +x docker-helper.sh
./docker-helper.sh build
./docker-helper.sh start
./docker-helper.sh cli
```

📖 **Guide complet**: [archive/docker_setup.md](archive/docker_setup.md)

### Installation manuelle (Python 3.10 ou 3.11)

```bash
# Cloner le dépôt
git clone https://github.com/MrrL0tus/Lotusette.git
cd Lotusette

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec vos clés API
```

### Utilisation

```bash
# Lancer l'interface CLI (à venir)
python -m lotusette.ui.cli

# Lancer le serveur API (à venir)
python -m lotusette.api.main

# Lancer l'interface web (à venir)
# python -m lotusette.ui.web
```

## 📚 Documentation

### 📖 Guides dans [archive/](archive/)

**Nouveau !** Documentation complète pour démarrer avec Lotusette:

1. **[Guide de Démarrage IA](archive/getting_started_ai.md)** - Votre première IA en 5 étapes
   - Pour les débutants qui créent leur première IA
   - Concepts fondamentaux expliqués simplement
   - Exemples de code complets

2. **[Guide Docker](archive/docker_setup.md)** - Solution pour Python 3.13
   - Résout les problèmes de compatibilité
   - Configuration Docker complète
   - Commandes et dépannage

3. **[Guide Modèles Locaux](archive/local_models_guide.md)** - IA sans cloud
   - Utiliser des modèles HuggingFace localement
   - Deux options: vLLM et Transformers
   - Configuration matérielle et optimisation

### 📋 Documentation générale

- [ROADMAP.md](ROADMAP.md) - Feuille de route détaillée du projet
- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture technique
- [CONTRIBUTING.md](CONTRIBUTING.md) - Guide de contribution
- [docs/](docs/) - Documentation technique détaillée

## 🛠️ Technologies

**Core**
- Python 3.10-3.11 (⚠️ 3.13 non supporté - utilisez Docker)
- FastAPI (API backend)
- PostgreSQL (base de données)
- Docker (environnement isolé)

**AI/ML**
- OpenAI API / Claude (LLM cloud)
- **Nouveau !** Modèles locaux HuggingFace (vLLM, Transformers)
- LangChain (framework)
- Whisper (STT)
- Coqui TTS (TTS)
- ChromaDB (vector database)

**Gaming**
- PyAutoGUI (automation)
- OpenCV (computer vision)
- Stable-Baselines3 (RL)

**Robotique** (futur)
- ROS 2
- PyBullet

## 🎯 État Actuel

🟢 **Phase 1 en cours**: Fondations de base

- [x] Initialisation du dépôt
- [x] Documentation de la roadmap
- [ ] Structure du projet
- [ ] Moteur conversationnel de base
- [ ] Système de mémoire initial

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer:

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails (à venir).

## 📝 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- Inspiré par le projet Neuro-sama
- Communauté open-source pour les outils et bibliothèques
- Contributeurs du projet

## 📧 Contact

MrrL0tus - [@MrrL0tus](https://github.com/MrrL0tus)

Lien du projet: [https://github.com/MrrL0tus/Lotusette](https://github.com/MrrL0tus/Lotusette)

---

**Note**: Ce projet est en développement actif. La roadmap et les fonctionnalités peuvent évoluer.