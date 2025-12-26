# 🚀 Guide de Démarrage Rapide - Utiliser un LLM Local en 5 Minutes

Ce guide ultra-rapide vous permet de lancer Lotusette avec un modèle local HuggingFace en quelques minutes.

## ⚡ Version Express (Docker - Recommandé)

### Étape 1: Installation Docker (si pas déjà fait)
```bash
# Linux/Mac
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Windows: téléchargez Docker Desktop
# https://www.docker.com/products/docker-desktop
```

### Étape 2: Setup Lotusette
```bash
# Cloner et construire
git clone https://github.com/MrrL0tus/Lotusette.git
cd Lotusette
chmod +x docker-helper.sh
./docker-helper.sh build

# Démarrer les services
./docker-helper.sh start
```

### Étape 3: Lancer votre premier modèle local
```bash
# Entrer dans le container
./docker-helper.sh shell

# Lancer l'exemple avec Phi-2 (petit modèle, ~3GB)
python examples/local_models_example.py
# Choisir option 1
```

**C'est tout!** Le modèle sera téléchargé automatiquement la première fois (peut prendre 5-10 minutes selon votre connexion).

---

## 🔧 Version Sans Docker (Python 3.11 requis)

### Prérequis
```bash
# Vérifier votre version Python
python --version
# Doit afficher Python 3.10.x ou 3.11.x
# Si vous avez 3.13, utilisez Docker!
```

### Étape 1: Installation
```bash
# Cloner le projet
git clone https://github.com/MrrL0tus/Lotusette.git
cd Lotusette

# Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Étape 2: Installer les dépendances modèles locaux
```bash
# PyTorch (CPU)
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Ou PyTorch (GPU - CUDA 11.8)
pip install torch --index-url https://download.pytorch.org/whl/cu118

# Autres dépendances
pip install transformers accelerate bitsandbytes
```

### Étape 3: Lancer l'exemple
```bash
# Créer dossier pour modèles
mkdir -p data/models

# Lancer
python examples/local_models_example.py
# Choisir option 1
```

---

## 📝 Utilisation dans votre code

Une fois que vous avez testé l'exemple, voici comment utiliser les modèles locaux dans votre propre code:

### Script minimal (5 lignes!)
```python
import asyncio
from lotusette.core.llm import LLMFactory

async def main():
    # Créer le provider
    llm = LLMFactory.create_provider(
        provider_name="local-transformers",
        model="microsoft/phi-2",
        cache_dir="./data/models"
    )
    
    # Poser une question
    messages = [llm.create_message("user", "Bonjour! Qui es-tu?")]
    response = await llm.generate(messages)
    print(response.content)

asyncio.run(main())
```

Sauvegardez dans `test.py` et lancez avec `python test.py`.

---

## 🎯 Modèles recommandés pour débuter

### 1. microsoft/phi-2 (2.7B) ⭐ RECOMMANDÉ POUR DÉBUTER
- **Taille**: ~5GB téléchargement
- **VRAM**: 4-6GB (ou CPU)
- **Qualité**: Excellente pour la taille
- **Vitesse**: Rapide même sur CPU
```python
model="microsoft/phi-2"
```

### 2. TinyLlama/TinyLlama-1.1B-Chat-v1.0 (1.1B)
- **Taille**: ~2GB téléchargement
- **VRAM**: 2-3GB (ou CPU)
- **Qualité**: Bonne pour des tâches simples
- **Vitesse**: Très rapide
```python
model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
```

### 3. mistralai/Mistral-7B-Instruct-v0.2 (7B)
- **Taille**: ~14GB téléchargement
- **VRAM**: 12-16GB (GPU requis)
- **Qualité**: Excellente, proche de GPT-3.5
- **Vitesse**: Moyenne
```python
model="mistralai/Mistral-7B-Instruct-v0.2"
# Avec quantification pour économiser VRAM:
llm = LLMFactory.create_provider(
    provider_name="local-transformers",
    model="mistralai/Mistral-7B-Instruct-v0.2",
    load_in_8bit=True  # Réduit l'utilisation mémoire de ~50%
)
```

---

## 🔥 Option Avancée: Utiliser vLLM (Plus performant)

Si vous voulez les meilleures performances avec un modèle 7B+:

### Étape 1: Installer vLLM
```bash
# Nécessite un GPU NVIDIA
pip install vllm
```

### Étape 2: Démarrer le serveur
```bash
# Terminal 1: Lancer le serveur vLLM
python -m vllm.entrypoints.openai.api_server \
    --model mistralai/Mistral-7B-Instruct-v0.2 \
    --host 0.0.0.0 \
    --port 8001
```

### Étape 3: Utiliser dans votre code
```python
# Terminal 2: Votre code Python
import asyncio
from lotusette.core.llm import LLMFactory

async def main():
    llm = LLMFactory.create_provider(
        provider_name="local-vllm",
        model="mistralai/Mistral-7B-Instruct-v0.2",
        base_url="http://localhost:8001/v1"
    )
    
    messages = [llm.create_message("user", "Explique-moi l'IA")]
    response = await llm.generate(messages)
    print(response.content)

asyncio.run(main())
```

---

## ❓ FAQ Rapide

### "Le téléchargement est lent?"
C'est normal la première fois. Les modèles sont gros (2-15GB). Une fois téléchargés, ils sont mis en cache dans `./data/models` et les prochains lancements seront instantanés.

### "Out of Memory / CUDA OOM?"
Utilisez un modèle plus petit ou la quantification:
```python
load_in_8bit=True  # Dans create_provider
```

### "Ça marche pas sur CPU?"
CPU fonctionne mais est **très lent**. Privilégiez les petits modèles (Phi-2, TinyLlama).

### "Comment changer la personnalité?"
```python
messages = [
    llm.create_message("system", "Tu es un pirate qui parle en vers"),
    llm.create_message("user", "Bonjour!")
]
```

### "Les réponses sont bizarres/en anglais?"
Ajoutez un message système en français:
```python
messages = [
    llm.create_message("system", "Tu DOIS toujours répondre en français."),
    llm.create_message("user", "Hello!")
]
```

---

## 📚 Pour aller plus loin

- **Guide complet**: [archive/local_models_guide.md](local_models_guide.md)
- **Créer votre IA**: [archive/getting_started_ai.md](getting_started_ai.md)
- **Configuration Docker**: [archive/docker_setup.md](docker_setup.md)

---

## 🆘 Besoin d'aide?

1. Consultez les guides détaillés dans `archive/`
2. Ouvrez une issue sur GitHub
3. Vérifiez que vous utilisez Python 3.10 ou 3.11 (pas 3.13!)

---

**Temps total de setup**: 10-15 minutes (dont téléchargement modèle)  
**Difficulté**: Débutant  
**Prérequis**: Docker OU Python 3.11

Bon courage! 🚀
