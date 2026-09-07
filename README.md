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
└── ui/                # Interfaces utilisateur

data/                  # Données et modèles (hors package)
tests/                 # Tests
```

## 🚀 Démarrage rapide

### Prérequis

- Python 3.10 ou plus récent (3.13 inclus)
- `pip`
- Pour le mode local : un serveur d'inférence compatible OpenAI
  ([llama.cpp](https://github.com/ggml-org/llama.cpp) ou
  [Ollama](https://ollama.com)). Aucun GPU n'est obligatoire.

Aucune clé d'API n'est nécessaire en mode local.

### Installation

```bash
git clone https://github.com/MrrL0tus/Lotusette.git
cd Lotusette

python -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate

pip install -r requirements.txt   # ~30 s, environ 230 Mo

cp .env.example .env              # fonctionne tel quel, rien à remplir
```

Les extras optionnels s'installent à la demande :

```bash
pip install -e ".[dev]"     # tests et outils de qualité
pip install -e ".[voice]"   # étape E6, pas encore implémenté
```

### Lancer un modèle en local

Installez llama.cpp, puis démarrez le serveur. `-hf` télécharge le modèle
directement depuis Hugging Face :

```bash
# Machine avec 12 Go de VRAM ou plus
llama-server -hf mistralai/Ministral-3-14B-Instruct-2512-GGUF:Q4_K_M \
  -c 16384 --port 8080 --host 127.0.0.1

# Machine plus modeste (6 Go de VRAM, ou CPU seul)
llama-server -hf mistralai/Ministral-3-3B-Instruct-2512-GGUF:Q4_K_M \
  -c 8192 --port 8080 --host 127.0.0.1
```

Vérifiez que le serveur répond :

```bash
curl http://localhost:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"local","messages":[{"role":"user","content":"salut"}]}'
```

📖 Choix du modèle selon votre machine : [docs/MODELS.md](docs/MODELS.md)

### Utilisation

```bash
python -m lotusette.ui.cli
```

La réponse s'affiche au fil de la génération. `Ctrl-C` interrompt une réponse
en cours sans quitter l'application.

### Utiliser une API distante à la place

```bash
# .env
LLM_PROVIDER=openai        # ou claude
OPENAI_API_KEY=sk-...
```

### Docker (optionnel)

Docker avait été ajouté pour contourner une dépendance qui imposait
Python < 3.12. Cette dépendance a été retirée : l'installation locale
fonctionne désormais sur toutes les versions supportées, et Docker n'est plus
qu'une commodité.

```bash
./docker-helper.sh build && ./docker-helper.sh cli
```

## 📚 Documentation

- [docs/MODELS.md](docs/MODELS.md) — choix du modèle local selon la machine
- [ROADMAP.md](ROADMAP.md) — feuille de route en 6 phases
- [ARCHITECTURE.md](ARCHITECTURE.md) — architecture technique (cible à long terme)
- [CONTRIBUTING.md](CONTRIBUTING.md) — guide de contribution
- [docs/phase1.md](docs/phase1.md) — état détaillé de la phase 1

Le répertoire [archive/](archive/) contient d'anciens guides, conservés pour
mémoire. Ils décrivent en partie du code qui n'existe plus (providers
Transformers et vLLM) : préférez `docs/` en cas de contradiction.

## 🛠️ Technologies

**Core**
- Python 3.10+
- SQLAlchemy + SQLite (mémoire long terme, aucun serveur à installer)
- rich (interface en ligne de commande)
- aiohttp (client du serveur LLM local)

**LLM**
- llama.cpp / Ollama pour l'inférence locale
- API OpenAI et Anthropic en option

**À venir** (voir ROADMAP.md)
- Piper (TTS) et faster-whisper (STT) — phase 2
- fastembed + sqlite-vec (mémoire sémantique) — phase 3
- FastAPI (API et interface web) — phase 4
- PyAutoGUI, OpenCV, Stable-Baselines3 (gaming) — phase 5
- ROS 2, PyBullet (robotique) — phase 6

## 🎯 État Actuel

🟢 **Phase 1 livrée**: Fondations de base

- [x] Initialisation du dépôt
- [x] Documentation de la roadmap
- [x] Structure du projet
- [x] Moteur conversationnel de base (local, OpenAI, Claude)
- [x] Système de mémoire initial (court terme en mémoire, long terme SQLite)
- [x] CLI avec affichage au fil de la génération
- [x] Suite de tests

🟡 **En cours**: la mémoire long terme est écrite mais pas encore relue au
démarrage. Reprise de session, budget de contexte en tokens et mémoire
sémantique constituent la suite (voir ROADMAP.md).

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer:

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails.

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