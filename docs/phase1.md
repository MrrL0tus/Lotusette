# Phase 1: Fondations de Base

Cette phase établit les fondements techniques du projet Lotusette.

## État au 7 septembre 2026

Phase 1 livrée sur ses critères de validation : conversation en local ou via
API, mémoire court et long terme, CLI avec affichage au fil de la génération,
95 tests au vert sur Python 3.11 et 3.13.

Deux limites connues, traitées à l'étape suivante :

- la mémoire long terme est écrite mais jamais relue au démarrage ;
- le contexte est tronqué par nombre de messages, pas par budget de tokens.

Le provider local (`LLM_PROVIDER=local`) parle à llama.cpp ou Ollama et ne
demande aucune clé d'API. Voir [MODELS.md](MODELS.md).

## Objectifs

1. **Infrastructure Core**
   - Structure modulaire du projet
   - Configuration et gestion des environnements
   - Logging et monitoring de base

2. **Moteur Conversationnel**
   - Intégration avec un LLM (OpenAI/Claude)
   - Gestion du contexte conversationnel
   - Interface CLI pour tests

3. **Système de Mémoire Initial**
   - Base de données pour conversations
   - Stockage et récupération de l'historique
   - Gestion du contexte

## Architecture Technique

### Structure du Projet

```
lotusette/
├── core/               # Fonctionnalités principales
│   ├── llm/           # Intégration LLM
│   ├── memory/        # Systèmes de mémoire
│   ├── personality/   # Gestion personnalité
│   └── config/        # Configuration
├── ui/                # Interfaces utilisateur
│   └── cli/           # Interface CLI
└── infrastructure/    # Infrastructure technique
    ├── database/      # Gestion BDD
    └── config/        # Configuration système
```

### Technologies

- **Python 3.10+**: Langage principal
- **LangChain**: Framework pour LLM
- **SQLAlchemy**: ORM pour la base de données
- **Pydantic**: Validation et configuration
- **FastAPI**: Framework API (préparation Phase 2)

## Implémentation

### Semaine 1: Setup Initial

- [x] Structure du projet
- [x] Configuration des dépendances
- [x] Système de configuration (Settings)
- [x] Logging setup — `logging` standard, sortie via `rich`
- [x] Tests de base

### Semaine 2-3: Moteur LLM

- [x] Interface abstraite LLM
- [x] Implémentation OpenAI
- [x] Implémentation Claude (optionnel)
- [x] Gestion des prompts système
- [ ] Gestion du contexte et tokens — troncature par nombre de messages seulement, pas encore par budget de tokens (voir E3)
- [x] Tests unitaires

### Semaine 4: Système de Mémoire

- [x] Modèles de base de données
- [ ] Repository pattern — non retenu, `LongTermMemory` accède directement à SQLAlchemy
- [x] Mémoire court terme (session)
- [x] Mémoire long terme (persistante)
- [x] Tests d'intégration

### Semaine 5: Interface CLI

- [x] Interface utilisateur CLI
- [x] Boucle conversationnelle
- [x] Gestion de l'historique
- [x] Commandes utilitaires
- [ ] Tests end-to-end — la boucle CLI complète n'est pas encore automatisée (le flux et les commandes le sont)

## Livrables

### Documentation
- [x] ROADMAP.md
- [x] ARCHITECTURE.md
- [x] CONTRIBUTING.md
- [x] README.md
- [ ] Documentation API (Sphinx) — reporté, l'API n'existe pas encore (voir E7)

### Code
- [x] Structure du projet
- [x] Configuration de base
- [x] Module LLM fonctionnel
- [x] Module Memory fonctionnel
- [x] CLI opérationnelle

### Tests
- [ ] Tests unitaires (coverage > 80%) — 95 tests au vert, couverture non mesurée formellement
- [x] Tests d'intégration
- [ ] Tests end-to-end — la boucle CLI complète n'est pas encore automatisée (le flux et les commandes le sont)

## Métriques de Succès

✅ **Critères de validation**:
- Conversation textuelle fluide avec le LLM
- Temps de réponse < 2 secondes
- Rétention du contexte sur 10+ échanges
- Tests passant avec > 80% de couverture
- Documentation complète et à jour

## Prochaines Étapes

Une fois la Phase 1 complétée, nous passerons à la **Phase 2: Capacités Vocales**.

---

**Statut actuel**: 🟢 En cours - Setup initial terminé
