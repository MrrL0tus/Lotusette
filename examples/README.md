# Exemples Lotusette

## 📚 Exemples disponibles

### [local_models_example.py](local_models_example.py)

Utilisation du provider LLM local, en génération classique puis en flux.

**Ce que ça démontre :**
- Création du provider `local` via `LLMFactory`
- Génération complète avec `generate()`
- Génération au fil de l'eau avec `generate_stream()`
- Mesure du temps jusqu'au premier token et du débit

**Prérequis :**
- Lotusette installé : `pip install -e .`
- Un serveur d'inférence compatible OpenAI qui tourne en face

**Utilisation :**

```bash
# 1. Démarrer le serveur d'inférence
llama-server -hf mistralai/Ministral-3-3B-Instruct-2512-GGUF:Q4_K_M \
  -c 8192 --port 8080 --host 127.0.0.1

# 2. Lancer l'exemple
python examples/local_models_example.py
```

Le serveur et le modèle se surchargent par variables d'environnement :

```bash
LOCAL_LLM_BASE_URL=http://autre-machine:8080/v1 \
LOCAL_LLM_MODEL=qwen3-8b \
python examples/local_models_example.py
```

Voir [docs/MODELS.md](../docs/MODELS.md) pour le choix du modèle selon la machine.

## 🚀 Ajouter vos propres exemples

1. Créez un fichier Python dans ce dossier
2. Ajoutez une docstring expliquant le prérequis et la commande de lancement
3. Documentez-le dans ce README
4. Vérifiez qu'il passe `make lint`

## 💡 Idées d'exemples futurs

- Reprise d'une conversation depuis la mémoire long terme (étape E3)
- Recherche sémantique dans l'historique (étape E4)
- Appel d'outils depuis le modèle (étape E5)
- Utilisation de l'API REST (étape E7)

---

Documentation principale : [../README.md](../README.md)
