# Guide des Modèles Locaux pour Lotusette

## 📋 Vue d'ensemble

Ce guide explique comment utiliser des modèles d'IA locaux avec Lotusette au lieu des APIs cloud (OpenAI, Claude).

## ❓ Pourquoi des modèles locaux ?

### Avantages
- 🔒 **Confidentialité**: Vos données restent sur votre machine
- 💰 **Coût**: Pas de frais d'API après l'achat du matériel
- ⚡ **Latence**: Pas de délai réseau
- 🌍 **Offline**: Fonctionne sans internet
- 🎨 **Personnalisation**: Possibilité de fine-tuner les modèles

### Inconvénients
- 💻 **Matériel**: Nécessite un GPU puissant (recommandé)
- 📦 **Espace disque**: Les modèles peuvent être très gros (7B = ~14GB, 20B = ~40GB)
- 🔧 **Complexité**: Configuration plus technique
- 🎯 **Performance**: Peut être moins performant que GPT-4

## 🎯 Deux approches disponibles

Lotusette supporte deux façons d'utiliser des modèles locaux:

### Option A: vLLM (Recommandé pour la production)
- **Meilleure performance** grâce à PagedAttention et continuous batching
- **API compatible OpenAI** - facile à intégrer
- **Optimisé pour l'inférence** sur GPU
- Idéal pour modèles moyens/grands (7B+)

### Option B: Transformers (Recommandé pour le développement)
- **Plus simple** - appel direct au modèle
- **Flexible** - facile à personnaliser
- **Moins de dépendances**
- Idéal pour petits modèles (<7B) ou expérimentation

## 🔧 Configuration matérielle recommandée

### Minimum (modèles petits: 1-3B)
- GPU: 6GB VRAM (GTX 1060, RTX 3060)
- RAM: 8GB
- Stockage: 50GB

### Recommandé (modèles moyens: 7B)
- GPU: 12GB VRAM (RTX 3060 12GB, RTX 4070)
- RAM: 16GB
- Stockage: 100GB

### Optimal (modèles grands: 13B+)
- GPU: 24GB VRAM (RTX 3090, RTX 4090, A5000)
- RAM: 32GB+
- Stockage: 200GB+

### Sans GPU (CPU uniquement)
- Possible mais **très lent**
- Utilisez de petits modèles (1-3B)
- Considérez la quantification (4-bit, 8-bit)

## 📦 Option A: Utiliser vLLM

### 1. Installation de vLLM

```bash
# Dans Docker (recommandé)
./docker-helper.sh shell
pip install vllm

# Ou en local
pip install vllm
```

### 2. Démarrer un serveur vLLM

```bash
# Exemple avec Mistral-7B
python -m vllm.entrypoints.openai.api_server \
    --model mistralai/Mistral-7B-Instruct-v0.2 \
    --host 0.0.0.0 \
    --port 8001 \
    --dtype float16

# Avec quantification 8-bit (économie de VRAM)
python -m vllm.entrypoints.openai.api_server \
    --model mistralai/Mistral-7B-Instruct-v0.2 \
    --host 0.0.0.0 \
    --port 8001 \
    --quantization awq
```

### 3. Configuration dans Lotusette

Éditez votre `.env`:
```bash
LLM_PROVIDER=local-vllm
LLM_MODEL=mistralai/Mistral-7B-Instruct-v0.2
VLLM_BASE_URL=http://localhost:8001/v1
```

### 4. Utilisation

```python
from lotusette.core.llm import LLMFactory

# Créer un provider vLLM
llm = LLMFactory.create_provider(
    provider_name="local-vllm",
    model="mistralai/Mistral-7B-Instruct-v0.2",
    base_url="http://localhost:8001/v1",
    temperature=0.7,
    max_tokens=1000,
)

# Utiliser comme n'importe quel provider
messages = [
    llm.create_message("system", "Tu es Lotusette, une IA amicale."),
    llm.create_message("user", "Bonjour!"),
]
response = await llm.generate(messages)
print(response.content)
```

## 📦 Option B: Utiliser Transformers directement

### 1. Installation des dépendances

```bash
# Dans Docker
./docker-helper.sh shell
pip install torch transformers accelerate bitsandbytes

# Ou en local
pip install torch transformers accelerate bitsandbytes
```

### 2. Configuration dans Lotusette

Éditez votre `.env`:
```bash
LLM_PROVIDER=local-transformers
LLM_MODEL=microsoft/phi-2
MODELS_CACHE_DIR=/app/data/models
```

### 3. Utilisation

```python
from lotusette.core.llm import LLMFactory

# Créer un provider Transformers
llm = LLMFactory.create_provider(
    provider_name="local-transformers",
    model="microsoft/phi-2",  # ou TinyLlama/TinyLlama-1.1B-Chat-v1.0
    cache_dir="/app/data/models",
    temperature=0.7,
    max_tokens=500,
    # Options de quantification
    load_in_8bit=False,  # True pour économiser de la VRAM
    load_in_4bit=False,  # True pour économiser encore plus
)

# Utiliser
messages = [
    llm.create_message("user", "Explique-moi ce qu'est l'IA"),
]
response = await llm.generate(messages)
print(response.content)
```

## 🤖 Modèles recommandés

### Petits modèles (1-3B) - Bon pour débuter
- **microsoft/phi-2** (2.7B): Excellent rapport qualité/taille
- **TinyLlama/TinyLlama-1.1B-Chat-v1.0** (1.1B): Très rapide
- **stabilityai/stablelm-2-1_6b** (1.6B): Bonne performance

### Modèles moyens (7B) - Recommandé
- **mistralai/Mistral-7B-Instruct-v0.2** (7B): Excellent choix général
- **meta-llama/Llama-2-7b-chat-hf** (7B): Très populaire
- **microsoft/Phi-3-medium-4k-instruct** (14B): Très performant

### Grands modèles (13B+) - Si GPU puissant
- **mistralai/Mixtral-8x7B-Instruct-v0.1** (47B): Très performant
- **meta-llama/Llama-2-13b-chat-hf** (13B): Robuste
- **openai/gpt-oss-20b** (20B): Si disponible

### Pour la voix française
- **facebook/mms-tts-fra**: Text-to-Speech en français
- **jonatasgrosman/wav2vec2-large-xlsr-53-french**: Speech-to-Text

## 🎮 Exemple complet: Projet avec modèle local

### Structure du projet
```
Lotusette/
├── data/
│   └── models/          # Cache des modèles téléchargés
├── .env                 # Configuration
└── docker-compose.yml   # Services
```

### Fichier .env
```bash
# Provider LLM
LLM_PROVIDER=local-transformers
LLM_MODEL=microsoft/phi-2
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000

# Chemins
MODELS_CACHE_DIR=/app/data/models
DATA_DIR=/app/data

# Options de performance
USE_8BIT_QUANTIZATION=false
USE_4BIT_QUANTIZATION=false
```

### Script de test
```python
# test_local_model.py
import asyncio
from lotusette.core.llm import LLMFactory

async def main():
    # Créer le provider
    llm = LLMFactory.create_provider(
        provider_name="local-transformers",
        model="microsoft/phi-2",
        cache_dir="./data/models",
        temperature=0.7,
    )
    
    # Tester
    messages = [
        llm.create_message("system", "Tu es Lotusette, une IA sympathique."),
        llm.create_message("user", "Présente-toi!"),
    ]
    
    print("Génération en cours...")
    response = await llm.generate(messages)
    print(f"\nLotusette: {response.content}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🐛 Dépannage

### Out of Memory (OOM)
```python
# Solution 1: Utiliser la quantification 8-bit
llm = LLMFactory.create_provider(
    provider_name="local-transformers",
    model="mistralai/Mistral-7B-Instruct-v0.2",
    load_in_8bit=True,
)

# Solution 2: Utiliser un modèle plus petit
llm = LLMFactory.create_provider(
    provider_name="local-transformers",
    model="microsoft/phi-2",  # 2.7B au lieu de 7B
)
```

### Modèle lent
```bash
# Vérifier que CUDA est disponible
python -c "import torch; print(torch.cuda.is_available())"

# Si False, installer PyTorch avec CUDA
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Erreur de téléchargement
```bash
# Utiliser un miroir HuggingFace
export HF_ENDPOINT=https://hf-mirror.com
```

## 📚 Ressources

- [vLLM Documentation](https://docs.vllm.ai/)
- [HuggingFace Models](https://huggingface.co/models)
- [Transformers Documentation](https://huggingface.co/docs/transformers)
- [Guide quantification](https://huggingface.co/docs/transformers/main_classes/quantization)

## 🎯 Prochaines étapes

1. ✅ Comprendre les options locales
2. 🚀 Consultez [getting_started_ai.md](getting_started_ai.md) pour créer votre IA
3. 💬 Testez différents modèles pour trouver le meilleur pour votre usage

---

**Date de création**: 2025-12-26  
**Dernière mise à jour**: 2025-12-26  
**Providers supportés**: vLLM, Transformers
