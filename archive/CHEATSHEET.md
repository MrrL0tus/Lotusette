# 📋 Aide-Mémoire Complet - Lotusette avec Modèles Locaux

## 🐳 Commandes Docker

### Installation et Setup
```bash
# Construire l'image Docker
./docker-helper.sh build

# Démarrer les services (PostgreSQL, Redis)
./docker-helper.sh start

# Arrêter les services
./docker-helper.sh stop

# Redémarrer
./docker-helper.sh restart
```

### Utilisation
```bash
# Ouvrir un shell dans le container
./docker-helper.sh shell

# Lancer l'interface CLI
./docker-helper.sh cli

# Voir les logs
./docker-helper.sh logs

# Nettoyer tout (⚠️ supprime les données)
./docker-helper.sh clean
```

### Alternative: Docker Compose direct
```bash
# Construire
docker-compose build

# Démarrer en arrière-plan
docker-compose up -d

# Voir les logs en temps réel
docker-compose logs -f lotusette

# Arrêter
docker-compose down

# Exécuter une commande
docker-compose run --rm lotusette python examples/local_models_example.py
```

---

## 🤖 Commandes pour les Modèles Locaux

### Option A: vLLM (Serveur local haute performance)

#### Installation
```bash
pip install vllm
```

#### Démarrer un serveur vLLM
```bash
# Mistral-7B (recommandé)
python -m vllm.entrypoints.openai.api_server \
    --model mistralai/Mistral-7B-Instruct-v0.2 \
    --host 0.0.0.0 \
    --port 8001 \
    --dtype float16

# Phi-2 (plus petit)
python -m vllm.entrypoints.openai.api_server \
    --model microsoft/phi-2 \
    --host 0.0.0.0 \
    --port 8001

# Avec quantification AWQ (économie VRAM)
python -m vllm.entrypoints.openai.api_server \
    --model TheBloke/Mistral-7B-Instruct-v0.2-AWQ \
    --host 0.0.0.0 \
    --port 8001 \
    --quantization awq
```

#### Tester le serveur vLLM
```bash
# Vérifier que le serveur répond
curl http://localhost:8001/v1/models

# Test de génération
curl http://localhost:8001/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistralai/Mistral-7B-Instruct-v0.2",
    "prompt": "Bonjour, comment vas-tu?",
    "max_tokens": 50
  }'
```

### Option B: Transformers (Chargement direct)

#### Installation
```bash
# PyTorch CPU
pip install torch --index-url https://download.pytorch.org/whl/cpu

# PyTorch GPU (CUDA 11.8)
pip install torch --index-url https://download.pytorch.org/whl/cu118

# PyTorch GPU (CUDA 12.1)
pip install torch --index-url https://download.pytorch.org/whl/cu121

# Dépendances
pip install transformers accelerate bitsandbytes
```

#### Utilisation directe
```bash
# Lancer l'exemple
python examples/local_models_example.py

# Ou créer votre propre script
python mon_script.py
```

---

## 💻 Code Python - Exemples d'Utilisation

### 1. Transformers - Script Minimal
```python
import asyncio
from lotusette.core.llm import LLMFactory

async def main():
    llm = LLMFactory.create_provider(
        provider_name="local-transformers",
        model="microsoft/phi-2",
        cache_dir="./data/models"
    )
    
    messages = [llm.create_message("user", "Bonjour!")]
    response = await llm.generate(messages)
    print(response.content)

asyncio.run(main())
```

### 2. vLLM - Script Minimal
```python
import asyncio
from lotusette.core.llm import LLMFactory

async def main():
    llm = LLMFactory.create_provider(
        provider_name="local-vllm",
        model="mistralai/Mistral-7B-Instruct-v0.2",
        base_url="http://localhost:8001/v1"
    )
    
    messages = [llm.create_message("user", "Bonjour!")]
    response = await llm.generate(messages)
    print(response.content)

asyncio.run(main())
```

### 3. Avec Personnalité
```python
import asyncio
from lotusette.core.llm import LLMFactory

async def main():
    llm = LLMFactory.create_provider(
        provider_name="local-transformers",
        model="microsoft/phi-2",
        cache_dir="./data/models"
    )
    
    messages = [
        llm.create_message("system", "Tu es Lotusette, une IA sympathique."),
        llm.create_message("user", "Qui es-tu?")
    ]
    response = await llm.generate(messages)
    print(response.content)

asyncio.run(main())
```

### 4. Avec Streaming (affichage mot par mot)
```python
import asyncio
from lotusette.core.llm import LLMFactory

async def main():
    llm = LLMFactory.create_provider(
        provider_name="local-transformers",
        model="microsoft/phi-2",
        cache_dir="./data/models"
    )
    
    messages = [llm.create_message("user", "Raconte-moi une histoire")]
    
    print("Réponse: ", end="", flush=True)
    async for chunk in llm.generate_stream(messages):
        print(chunk, end="", flush=True)
    print()

asyncio.run(main())
```

### 5. Avec Quantification (économie VRAM)
```python
import asyncio
from lotusette.core.llm import LLMFactory

async def main():
    llm = LLMFactory.create_provider(
        provider_name="local-transformers",
        model="mistralai/Mistral-7B-Instruct-v0.2",
        cache_dir="./data/models",
        load_in_8bit=True  # Réduit utilisation mémoire de ~50%
        # Ou: load_in_4bit=True  # Réduit de ~75%
    )
    
    messages = [llm.create_message("user", "Explique l'IA")]
    response = await llm.generate(messages)
    print(response.content)

asyncio.run(main())
```

### 6. Conversation Interactive
```python
import asyncio
from lotusette.core.llm import LLMFactory

async def main():
    llm = LLMFactory.create_provider(
        provider_name="local-transformers",
        model="microsoft/phi-2",
        cache_dir="./data/models"
    )
    
    conversation = [
        llm.create_message("system", "Tu es Lotusette.")
    ]
    
    print("Chatbot démarré! (tapez 'quit' pour quitter)\n")
    
    while True:
        user_input = input("Vous: ")
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        conversation.append(llm.create_message("user", user_input))
        response = await llm.generate(conversation)
        
        print(f"Lotusette: {response.content}\n")
        conversation.append(llm.create_message("assistant", response.content))

asyncio.run(main())
```

---

## 🔧 Configuration (.env)

### Pour vLLM
```bash
LLM_PROVIDER=local-vllm
VLLM_BASE_URL=http://localhost:8001/v1
VLLM_MODEL=mistralai/Mistral-7B-Instruct-v0.2
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
```

### Pour Transformers
```bash
LLM_PROVIDER=local-transformers
LOCAL_MODEL=microsoft/phi-2
MODELS_CACHE_DIR=./data/models
USE_8BIT_QUANTIZATION=false
USE_4BIT_QUANTIZATION=false
DEVICE=auto
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1000
```

---

## 🎯 Modèles HuggingFace Recommandés

### Petits (1-3B) - CPU OK
```python
"microsoft/phi-2"  # 2.7B - Excellent choix
"TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # 1.1B - Très rapide
"stabilityai/stablelm-2-1_6b"  # 1.6B
```

### Moyens (7B) - GPU 12GB+
```python
"mistralai/Mistral-7B-Instruct-v0.2"  # Recommandé
"meta-llama/Llama-2-7b-chat-hf"  # Populaire
"microsoft/Phi-3-medium-4k-instruct"  # 14B mais performant
```

### Grands (13B+) - GPU 24GB+
```python
"mistralai/Mixtral-8x7B-Instruct-v0.1"  # 47B - Très bon
"meta-llama/Llama-2-13b-chat-hf"  # 13B
```

---

## 🐛 Dépannage Rapide

### Vérifier version Python
```bash
python --version  # Doit être 3.10 ou 3.11, PAS 3.13!
```

### Vérifier CUDA (GPU)
```bash
python -c "import torch; print(f'CUDA disponible: {torch.cuda.is_available()}')"
python -c "import torch; print(f'Nombre de GPUs: {torch.cuda.device_count()}')"
```

### Nettoyer le cache des modèles
```bash
rm -rf ./data/models/*
```

### Voir l'espace disque
```bash
du -sh ./data/models/  # Espace utilisé par les modèles
df -h  # Espace disque total
```

### Tester l'import Python
```bash
python -c "from lotusette.core.llm import LLMFactory; print('OK')"
```

---

## 📚 Fichiers de Documentation

| Fichier | Description |
|---------|-------------|
| `archive/QUICKSTART_LOCAL_LLM.md` | Démarrage ultra-rapide (5 min) |
| `archive/local_models_guide.md` | Guide complet modèles locaux |
| `archive/getting_started_ai.md` | Guide pour créer votre première IA |
| `archive/docker_setup.md` | Configuration Docker complète |
| `archive/IMPLEMENTATION_SUMMARY_DOCKER_LOCAL_MODELS.md` | Résumé technique |
| `examples/local_models_example.py` | Exemple de code prêt à utiliser |

---

## 🎓 Paramètres Importants

### Temperature (créativité)
```python
temperature=0.0   # Très déterministe, toujours la même réponse
temperature=0.7   # Équilibré (défaut)
temperature=1.5   # Très créatif, peut divaguer
```

### Max Tokens (longueur)
```python
max_tokens=50    # Réponse très courte
max_tokens=500   # Réponse moyenne (défaut)
max_tokens=2000  # Réponse longue
```

### Quantification (mémoire)
```python
load_in_8bit=True   # Réduit VRAM de ~50%
load_in_4bit=True   # Réduit VRAM de ~75% (moins précis)
```

---

**Dernière mise à jour**: 2025-12-26  
**Version**: 1.0
