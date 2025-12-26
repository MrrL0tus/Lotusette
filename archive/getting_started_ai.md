# Guide de Démarrage - Créer votre Première IA

## 👋 Bienvenue !

Ce guide est conçu pour les débutants qui créent leur première IA. Nous allons vous guider étape par étape pour créer Lotusette, votre assistant IA personnel.

## 🎯 Qu'est-ce qu'une IA conversationnelle ?

Une IA conversationnelle est un programme capable de:
1. **Comprendre** ce que vous lui dites (en texte ou à l'oral)
2. **Réfléchir** à une réponse appropriée
3. **Répondre** de manière naturelle et cohérente
4. **Se souvenir** des conversations passées

## 🧩 Les composants principaux

### 1. Le LLM (Large Language Model)
C'est le "cerveau" de l'IA - le modèle qui génère les réponses.

**Options disponibles:**
- ☁️ **Cloud (facile)**: OpenAI GPT-4, Claude
  - ✅ Très performant
  - ✅ Facile à utiliser
  - ❌ Coûte de l'argent
  - ❌ Nécessite internet

- 💻 **Local (recommandé pour débuter)**: Phi-2, Mistral, TinyLlama
  - ✅ Gratuit après installation
  - ✅ Privé
  - ❌ Nécessite un bon PC
  - ❌ Moins performant que GPT-4

### 2. La Mémoire
Permet à l'IA de se souvenir de vos conversations.

**Deux types:**
- **Court terme**: Les dernières phrases de la conversation
- **Long terme**: Historique complet stocké en base de données

### 3. La Personnalité
Définit comment l'IA se comporte et répond.

**Exemples:**
- Ton amical ou professionnel
- Verbeux ou concis
- Humoristique ou sérieux

## 🚀 Votre Première IA en 5 étapes

### Étape 1: Installation de l'environnement

#### Option A: Avec Docker (Recommandé - Plus simple)
```bash
# 1. Installer Docker
# Visitez: https://docs.docker.com/get-docker/

# 2. Cloner le projet
git clone https://github.com/MrrL0tus/Lotusette.git
cd Lotusette

# 3. Construire l'environnement
./docker-helper.sh build

# C'est tout ! Python 3.11 et toutes les dépendances sont installées
```

#### Option B: Installation manuelle
```bash
# 1. Vérifier la version de Python (doit être 3.10 ou 3.11)
python --version

# Si vous avez Python 3.13, Docker est OBLIGATOIRE
# car certaines bibliothèques ne sont pas compatibles

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

### Étape 2: Choisir votre modèle

#### Pour débuter: Modèle local petit
```bash
# Éditer .env
cp .env.example .env
nano .env

# Ajouter:
LLM_PROVIDER=local-transformers
LLM_MODEL=microsoft/phi-2
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=500
```

**Phi-2** est un excellent choix pour débuter:
- Seulement 2.7B paramètres (petit)
- Fonctionne même sans GPU
- Bonne qualité de réponse

#### Alternative: API OpenAI (plus simple mais payant)
```bash
# Dans .env:
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-votre-clé-ici
LLM_MODEL=gpt-3.5-turbo  # Moins cher que GPT-4
```

### Étape 3: Créer votre script de test

Créez un fichier `my_first_ai.py`:

```python
"""
Mon premier chatbot IA avec Lotusette
"""
import asyncio
from lotusette.core.llm import LLMFactory

async def main():
    print("🚀 Démarrage de votre première IA...")
    
    # 1. Créer le modèle
    llm = LLMFactory.create_provider(
        provider_name="local-transformers",
        model="microsoft/phi-2",
        temperature=0.7,  # Créativité (0=robotique, 1=créatif)
        max_tokens=500,   # Longueur maximale de la réponse
    )
    
    print("✅ Modèle chargé!")
    
    # 2. Définir la personnalité
    system_message = llm.create_message(
        "system",
        """Tu es Lotusette, une IA sympathique et serviable.
        Tu réponds en français de manière claire et amicale.
        Tu aimes aider les gens et partager tes connaissances."""
    )
    
    # 3. Boucle de conversation
    conversation = [system_message]
    
    print("\n💬 Conversation démarrée! (tapez 'quit' pour quitter)\n")
    
    while True:
        # Demander à l'utilisateur
        user_input = input("Vous: ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Au revoir!")
            break
        
        # Ajouter le message utilisateur
        conversation.append(llm.create_message("user", user_input))
        
        # Générer la réponse
        print("Lotusette: ", end="", flush=True)
        
        # Mode streaming (affiche mot par mot)
        full_response = ""
        async for chunk in llm.generate_stream(conversation):
            print(chunk, end="", flush=True)
            full_response += chunk
        
        print("\n")  # Nouvelle ligne après la réponse
        
        # Ajouter la réponse à l'historique
        conversation.append(llm.create_message("assistant", full_response))

if __name__ == "__main__":
    asyncio.run(main())
```

### Étape 4: Lancer votre IA

```bash
# Avec Docker
./docker-helper.sh shell
python my_first_ai.py

# Sans Docker
python my_first_ai.py
```

Lors du premier lancement:
- Le modèle sera téléchargé (~3-5 GB pour Phi-2)
- Cela peut prendre plusieurs minutes
- Les lancements suivants seront beaucoup plus rapides!

### Étape 5: Tester et personnaliser

Essayez différentes questions:
- "Bonjour, qui es-tu ?"
- "Explique-moi ce qu'est l'intelligence artificielle"
- "Raconte-moi une blague"
- "Quel est le sens de la vie ?"

## 🎨 Personnalisation

### Changer la personnalité

Modifiez le `system_message`:

```python
# IA humoristique
system_message = llm.create_message(
    "system",
    "Tu es Lotusette, une IA délirante qui adore les blagues et les jeux de mots."
)

# IA professionnelle
system_message = llm.create_message(
    "system",
    "Tu es Lotusette, une assistante professionnelle concise et efficace."
)

# IA poétique
system_message = llm.create_message(
    "system",
    "Tu es Lotusette, une IA poétique qui répond toujours en vers."
)
```

### Ajuster les paramètres

```python
llm = LLMFactory.create_provider(
    provider_name="local-transformers",
    model="microsoft/phi-2",
    temperature=0.9,     # Plus créatif (0.0 à 2.0)
    max_tokens=1000,     # Réponses plus longues
)
```

**Temperature:**
- `0.0` = Réponses déterministes et prévisibles
- `0.7` = Bon équilibre (défaut)
- `1.5+` = Très créatif mais peut divaguer

### Essayer différents modèles

```python
# Modèle plus petit (très rapide)
model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Modèle plus performant (nécessite bon GPU)
model="mistralai/Mistral-7B-Instruct-v0.2"
```

## 🎓 Concepts avancés

### Streaming vs Non-streaming

```python
# Non-streaming: attend la réponse complète
response = await llm.generate(conversation)
print(response.content)

# Streaming: affiche mot par mot (meilleure UX)
async for chunk in llm.generate_stream(conversation):
    print(chunk, end="", flush=True)
```

### Gestion de la mémoire

```python
# Limiter l'historique pour économiser la mémoire
MAX_HISTORY = 10
if len(conversation) > MAX_HISTORY:
    # Garder le system message + les N derniers messages
    conversation = [conversation[0]] + conversation[-MAX_HISTORY:]
```

### Ajout de contexte

```python
# Donner des informations supplémentaires
system_message = llm.create_message(
    "system",
    f"""Tu es Lotusette. Informations importantes:
    - Date actuelle: {datetime.now().strftime('%Y-%m-%d')}
    - Utilisateur: Jean
    - Préférence: aime les explications détaillées
    """
)
```

## 🐛 Problèmes courants

### "CUDA out of memory"
```python
# Solution: Utiliser quantification 8-bit
llm = LLMFactory.create_provider(
    provider_name="local-transformers",
    model="microsoft/phi-2",
    load_in_8bit=True,  # Réduit l'utilisation de VRAM
)
```

### "Le modèle répond en anglais"
```python
# Insister dans le system message
system_message = llm.create_message(
    "system",
    "Tu DOIS TOUJOURS répondre en français, même si la question est en anglais."
)
```

### "Les réponses sont incohérentes"
```python
# Réduire la température
temperature=0.3  # Plus déterministe
```

### "C'est trop lent!"
```python
# Solutions:
# 1. Utiliser un modèle plus petit
model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# 2. Réduire max_tokens
max_tokens=200

# 3. Utiliser vLLM au lieu de Transformers (voir guide modèles locaux)
```

## 📚 Prochaines étapes

### Niveau Débutant ✅
- [x] Créer votre première IA
- [ ] Expérimenter avec différentes personnalités
- [ ] Tester plusieurs modèles
- [ ] Comprendre les paramètres (temperature, max_tokens)

### Niveau Intermédiaire
- [ ] Ajouter une mémoire persistante (base de données)
- [ ] Créer une interface web avec FastAPI
- [ ] Intégrer la synthèse vocale (TTS)
- [ ] Ajouter la reconnaissance vocale (STT)

### Niveau Avancé
- [ ] Fine-tuner un modèle sur vos propres données
- [ ] Implémenter RAG (Retrieval Augmented Generation)
- [ ] Créer des outils pour l'IA (recherche web, etc.)
- [ ] Déployer en production avec vLLM

## 🎯 Exemples de projets

### 1. Assistant Personnel
```python
# Gestion d'agenda, rappels, recherches
system = "Tu es un assistant qui aide à organiser ma journée"
```

### 2. Tuteur Éducatif
```python
# Aide aux devoirs, explications
system = "Tu es un tuteur patient qui explique les concepts simplement"
```

### 3. Compagnon de Jeu
```python
# Jeux de rôle, histoires interactives
system = "Tu es un maître de jeu créatif pour des aventures textuelles"
```

### 4. Thérapeute Virtuel
```python
# Écoute et soutien émotionnel
system = "Tu es un ami empathique qui écoute et conseille avec bienveillance"
```

## 🆘 Besoin d'aide ?

### Documentation
- 📖 [Guide Docker](docker_setup.md)
- 📖 [Guide Modèles Locaux](local_models_guide.md)
- 📚 [Documentation HuggingFace](https://huggingface.co/docs)

### Communauté
- 💬 [Ouvrir une issue](https://github.com/MrrL0tus/Lotusette/issues)
- 🌟 [Discussions GitHub](https://github.com/MrrL0tus/Lotusette/discussions)

### Ressources d'apprentissage
- [Cours IA gratuit (français)](https://openclassrooms.com/)
- [Introduction au Machine Learning](https://www.coursera.org/learn/machine-learning)
- [Guide Python pour débutants](https://docs.python.org/fr/3/tutorial/)

## 🎉 Félicitations !

Vous avez créé votre première IA conversationnelle ! 🚀

N'hésitez pas à expérimenter, modifier et personnaliser Lotusette selon vos besoins. L'apprentissage se fait par la pratique !

---

**Date de création**: 2025-12-26  
**Dernière mise à jour**: 2025-12-26  
**Niveau**: Débutant à Intermédiaire
