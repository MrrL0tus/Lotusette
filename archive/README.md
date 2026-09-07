# Archive — documentation historique

> [!WARNING]
> **Ces documents sont obsolètes et conservés pour mémoire.**
>
> Ils décrivent les providers `local-transformers` et `local-vllm`, remplacés
> par un provider unique `local` qui parle à llama.cpp ou Ollama, ainsi qu'une
> installation Docker qui n'est plus nécessaire. `torch`, `transformers`,
> `bitsandbytes`, `langchain`, `chromadb`, `redis` et `celery` ne sont plus
> des dépendances du projet.
>
> **En cas de contradiction, la documentation à jour fait foi :**
>
> | Sujet | Document à jour |
> |---|---|
> | Installation et démarrage | [../README.md](../README.md) |
> | Choix du modèle local | [../docs/MODELS.md](../docs/MODELS.md) |
> | État de la phase 1 | [../docs/phase1.md](../docs/phase1.md) |
> | Contribution et outillage | [../CONTRIBUTING.md](../CONTRIBUTING.md) |
> | Feuille de route | [../ROADMAP.md](../ROADMAP.md) |

## 📚 Guides disponibles

### 🚀 [Démarrage Ultra-Rapide](QUICKSTART_LOCAL_LLM.md) ⭐ NOUVEAU!
Guide express pour lancer un modèle local en 5 minutes.

**Contenu:**
- Installation Docker en 3 commandes
- Lancement du premier modèle (Phi-2)
- Script minimal (5 lignes de code)
- FAQ rapide

**Pour qui:** Débutants qui veulent tester rapidement, ou utilisateurs pressés.

### 📋 [Aide-Mémoire Complet](CHEATSHEET.md) ⭐ NOUVEAU!
Toutes les commandes et exemples de code en un seul endroit.

**Contenu:**
- Commandes Docker complètes
- Commandes vLLM et Transformers
- 6 exemples de code Python prêts à l'emploi
- Configuration .env
- Liste complète des modèles recommandés
- Dépannage rapide

**Pour qui:** Référence rapide pour tous les utilisateurs.

### 1. [Guide de Démarrage IA](getting_started_ai.md)
Guide complet pour créer votre première IA conversationnelle.

**Contenu:**
- Concepts fondamentaux
- Installation pas à pas
- Votre première IA en 5 étapes
- Personnalisation
- Exemples de projets
- Problèmes courants

**Pour qui:** Débutants qui créent leur première IA.

### 2. [Guide Docker](docker_setup.md)
Configuration Docker pour forcer Python 3.11 et résoudre les problèmes de compatibilité.

**Contenu:**
- Pourquoi Docker ?
- Installation et configuration
- Commandes disponibles
- Dépannage

**Pour qui:** Tous les utilisateurs, surtout ceux qui rencontrent des problèmes de compatibilité Python.

### 3. [Guide Modèles Locaux](local_models_guide.md)
Utilisation de modèles d'IA locaux (HuggingFace, vLLM) au lieu des APIs cloud.

**Contenu:**
- Comparaison vLLM vs Transformers
- Configuration matérielle recommandée
- Installation et utilisation
- Modèles recommandés
- Dépannage

**Pour qui:** Utilisateurs souhaitant plus de confidentialité, économiser sur les coûts d'API, ou travailler offline.

### 4. [Résumé d'Implémentation](IMPLEMENTATION_SUMMARY_DOCKER_LOCAL_MODELS.md)
Documentation technique de l'implémentation Docker et modèles locaux.

**Contenu:**
- Problème résolu (Issue #3)
- Fichiers créés et modifications
- Architecture des nouveaux providers
- Statistiques et métriques

**Pour qui:** Développeurs et contributeurs voulant comprendre l'implémentation technique.

## 📅 Historique des documents

| Document | Date de création | Dernière MAJ | Version |
|----------|-----------------|--------------|---------|
| QUICKSTART_LOCAL_LLM.md | 2025-12-26 | 2025-12-26 | 1.0 |
| CHEATSHEET.md | 2025-12-26 | 2025-12-26 | 1.0 |
| docker_setup.md | 2025-12-26 | 2025-12-26 | 1.0 |
| local_models_guide.md | 2025-12-26 | 2025-12-26 | 1.0 |
| getting_started_ai.md | 2025-12-26 | 2025-12-26 | 1.0 |
| IMPLEMENTATION_SUMMARY_DOCKER_LOCAL_MODELS.md | 2025-12-26 | 2025-12-26 | 1.0 |

## 🔄 Mises à jour futures

Aucune. Ce dossier est figé. La documentation vivante est dans
[`docs/`](../docs/) et à la racine du dépôt.

## 📖 Autres ressources

- [README principal](../README.md)
- [Roadmap du projet](../ROADMAP.md)
- [Architecture](../ARCHITECTURE.md)
- [Guide de contribution](../CONTRIBUTING.md)

---

**Objectif de ce dossier :** conserver la trace des choix techniques
antérieurs. Ne pas suivre ces guides pour installer ou configurer le projet.
