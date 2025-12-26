# Exemples Lotusette

Ce dossier contient des exemples d'utilisation de Lotusette.

## 📚 Exemples disponibles

### [local_models_example.py](local_models_example.py)
Démontre l'utilisation des modèles LLM locaux avec Lotusette.

**Fonctionnalités démontrées:**
- Utilisation du provider `local-transformers` avec un modèle HuggingFace
- Génération de réponses
- Création de conversations

**Utilisation:**
```bash
# Avec Docker (recommandé)
./docker-helper.sh shell
python examples/local_models_example.py

# Sans Docker
python examples/local_models_example.py
```

**Prérequis:**
- Python 3.11 (ou Docker)
- Dépendances installées: `torch`, `transformers`, `accelerate`
- GPU recommandé (mais fonctionne sur CPU)

## 🚀 Ajouter vos propres exemples

Pour contribuer avec vos propres exemples:

1. Créez un nouveau fichier Python dans ce dossier
2. Ajoutez une docstring claire en haut du fichier
3. Documentez l'exemple dans ce README
4. Assurez-vous que le code est bien commenté

## 💡 Idées d'exemples futurs

- Utilisation avec l'API REST
- Intégration de la mémoire à long terme
- Utilisation de la voix (STT/TTS)
- Création d'un chatbot avec personnalité personnalisée
- Utilisation de RAG avec ChromaDB
- Fine-tuning d'un modèle local

---

Pour plus d'informations, consultez la [documentation principale](../archive/).
