# Architecture Technique - Lotusette

## Vue d'ensemble de l'architecture

Lotusette est conçue comme une architecture modulaire et extensible permettant l'ajout progressif de fonctionnalités tout en maintenant une base solide.

## Principes de conception

1. **Modularité**: Chaque composant est indépendant et peut être développé/testé séparément
2. **Extensibilité**: Facilité d'ajout de nouvelles capacités sans refactorisation majeure
3. **Scalabilité**: Architecture permettant la montée en charge
4. **Testabilité**: Facilité de tests unitaires et d'intégration
5. **Maintenabilité**: Code clair et bien documenté

## Architecture en couches

```
┌─────────────────────────────────────────────────┐
│           Interfaces Utilisateur                │
│  (CLI, Web UI, Desktop App, Voice Interface)    │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│              API Layer                          │
│     (REST API, WebSocket, Event Bus)            │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│          Application Layer                      │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ Conversation │  │   Actions    │            │
│  │  Manager     │  │   Executor   │            │
│  └──────────────┘  └──────────────┘            │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│            Core Services                        │
│  ┌──────┐ ┌────────┐ ┌──────────┐ ┌─────────┐ │
│  │ LLM  │ │ Memory │ │Personality│ │ Tools   │ │
│  └──────┘ └────────┘ └──────────┘ └─────────┘ │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│          Domain Services                        │
│  ┌──────┐ ┌──────┐ ┌────────┐ ┌──────────────┐ │
│  │Voice │ │ Web  │ │ Gaming │ │  Robotics    │ │
│  └──────┘ └──────┘ └────────┘ └──────────────┘ │
└───────────────────┬─────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────┐
│         Infrastructure Layer                    │
│  (Database, Cache, Queue, Storage, Config)      │
└─────────────────────────────────────────────────┘
```

## Composants détaillés

### 1. Core Services

#### 1.1 LLM Service
**Responsabilité**: Gestion des interactions avec les modèles de langage

```python
core/llm/
├── __init__.py
├── base.py              # Interface abstraite LLM
├── openai_provider.py   # Implémentation OpenAI
├── claude_provider.py   # Implémentation Anthropic
├── local_provider.py    # Modèles locaux (LLaMA, etc.)
├── prompt_manager.py    # Gestion des prompts système
└── token_manager.py     # Gestion des tokens et contexte
```

**Fonctionnalités**:
- Abstraction des différents fournisseurs LLM
- Gestion du contexte et des tokens
- Streaming de réponses
- Retry logic et fallback
- Caching des réponses

#### 1.2 Memory Service
**Responsabilité**: Gestion de la mémoire court et long terme

```python
core/memory/
├── __init__.py
├── base.py              # Interface abstraite mémoire
├── short_term.py        # Mémoire de session
├── long_term.py         # Mémoire persistante
├── episodic.py          # Mémoire épisodique (RAG)
├── semantic_search.py   # Recherche sémantique
└── embeddings.py        # Gestion des embeddings
```

**Types de mémoire**:
- **Court terme**: Contexte de conversation actuel (in-memory)
- **Long terme**: Base de données des conversations (PostgreSQL)
- **Épisodique**: Recherche sémantique dans l'historique (Vector DB)
- **Procédurale**: Compétences et comportements appris

#### 1.3 Personality Service
**Responsabilité**: Définition et évolution de la personnalité

```python
core/personality/
├── __init__.py
├── traits.py            # Traits de personnalité
├── behaviors.py         # Comportements
├── emotions.py          # Système émotionnel
└── evolution.py         # Évolution de la personnalité
```

**Aspects**:
- Traits de base (curiosité, humour, empathie)
- Réponses émotionnelles contextuelles
- Évolution basée sur les interactions
- Consistance de la personnalité

#### 1.4 Tools Service
**Responsabilité**: Gestion des outils et capacités

```python
core/tools/
├── __init__.py
├── registry.py          # Registre des outils
├── executor.py          # Exécution d'outils
├── validator.py         # Validation des paramètres
└── tools/               # Outils individuels
    ├── calculator.py
    ├── web_search.py
    └── ...
```

### 2. Domain Services

#### 2.1 Voice Service

```python
voice/
├── __init__.py
├── stt/
│   ├── whisper_stt.py
│   ├── google_stt.py
│   └── local_stt.py
├── tts/
│   ├── coqui_tts.py
│   ├── elevenlabs_tts.py
│   └── google_tts.py
└── audio/
    ├── capture.py       # Capture microphone
    ├── playback.py      # Lecture audio
    ├── processing.py    # Traitement signal
    └── vad.py           # Voice Activity Detection
```

#### 2.2 Web Service

```python
web/
├── __init__.py
├── search/
│   ├── google.py
│   ├── bing.py
│   └── duckduckgo.py
├── scraper/
│   ├── html_parser.py
│   ├── selenium_driver.py
│   └── content_extractor.py
└── tools/
    ├── web_browser.py
    ├── api_caller.py
    └── validator.py
```

#### 2.3 Gaming Service

```python
gaming/
├── __init__.py
├── vision/
│   ├── screen_capture.py
│   ├── ocr.py
│   └── object_detection.py
├── control/
│   ├── keyboard.py
│   ├── mouse.py
│   └── gamepad.py
└── agents/
    ├── base_agent.py
    ├── rl_agent.py      # Reinforcement Learning
    └── rule_based.py    # Agents basés sur règles
```

#### 2.4 Robotics Service (Futur)

```python
robotics/
├── __init__.py
├── hardware/
│   ├── ros_interface.py
│   ├── serial_comm.py
│   └── driver.py
├── control/
│   ├── motion.py
│   ├── manipulation.py
│   └── navigation.py
└── perception/
    ├── cameras.py
    ├── lidar.py
    └── sensors.py
```

### 3. API Layer

```python
api/
├── __init__.py
├── main.py              # Point d'entrée FastAPI
├── routes/
│   ├── chat.py          # Endpoints conversation
│   ├── voice.py         # Endpoints voix
│   ├── memory.py        # Endpoints mémoire
│   └── tools.py         # Endpoints outils
├── websocket/
│   ├── chat_ws.py       # WebSocket temps réel
│   └── voice_ws.py      # WebSocket audio
├── middleware/
│   ├── auth.py
│   ├── rate_limit.py
│   └── logging.py
└── models/              # Pydantic models
    ├── requests.py
    └── responses.py
```

### 4. User Interfaces

```python
ui/
├── cli/
│   ├── __init__.py
│   └── main.py          # Interface ligne de commande
├── web/
│   ├── frontend/        # React/Vue.js
│   └── backend/         # Backend pour le web
└── desktop/
    └── electron/        # Application Electron
```

### 5. Infrastructure

```python
infrastructure/
├── database/
│   ├── postgres.py      # PostgreSQL
│   ├── vector_db.py     # ChromaDB/Pinecone
│   └── migrations/
├── cache/
│   └── redis.py
├── queue/
│   └── task_queue.py    # Celery/RQ
├── storage/
│   ├── local.py
│   └── s3.py
└── config/
    ├── settings.py
    └── env.py
```

## Flux de données

### Conversation textuelle

```
User Input → API → Conversation Manager → Memory (retrieve context)
                                        ↓
                            LLM Service (generate response)
                                        ↓
                            Memory (store exchange)
                                        ↓
Response → API → User
```

### Conversation vocale

```
Audio Input → STT → Text → [Flux conversation textuelle] → Text → TTS → Audio Output
```

### Action avec outils

```
User Request → LLM (function calling) → Tools Executor
                                              ↓
                                      Execute Tool(s)
                                              ↓
                                      Result → LLM
                                              ↓
                                      Final Response
```

## Patterns de conception utilisés

1. **Repository Pattern**: Accès aux données via interfaces
2. **Factory Pattern**: Création des providers LLM, STT, TTS
3. **Strategy Pattern**: Différentes stratégies de mémoire
4. **Observer Pattern**: Événements et notifications
5. **Singleton Pattern**: Configuration et ressources partagées
6. **Dependency Injection**: IoC pour la testabilité

## Gestion des erreurs

```python
# Hiérarchie d'exceptions personnalisées
lotusette/exceptions/
├── __init__.py
├── base.py              # LotsusetteException
├── llm.py               # LLMException, TokenLimitException
├── memory.py            # MemoryException
├── voice.py             # VoiceException, STTException, TTSException
└── tools.py             # ToolException, ToolExecutionException
```

**Stratégies**:
- Retry avec backoff exponentiel pour les APIs
- Fallback vers providers alternatifs
- Graceful degradation
- Logging détaillé des erreurs

## Monitoring et observabilité

- **Logging**: Structured logging (JSON)
- **Metrics**: Prometheus
- **Tracing**: OpenTelemetry
- **Health checks**: Endpoints de santé pour chaque service

## Sécurité

- **Authentification**: JWT tokens
- **Autorisation**: Role-based access control (RBAC)
- **Rate limiting**: Protection contre abus
- **Input validation**: Validation stricte des entrées
- **Secrets management**: Variables d'environnement, vault
- **Sandboxing**: Exécution sécurisée des outils

## Performance

- **Caching**: Redis pour résultats fréquents
- **Connection pooling**: PostgreSQL, HTTP
- **Async/await**: I/O non-bloquant
- **Load balancing**: Distribution de charge
- **Batch processing**: Traitement par lots quand possible

## Scalabilité

- **Horizontal scaling**: API stateless
- **Queue-based processing**: Tâches asynchrones
- **Database sharding**: Si nécessaire
- **CDN**: Assets statiques
- **Microservices**: Possibilité de séparer les services

## Configuration

```python
# Exemple de configuration
class Settings(BaseSettings):
    # Application
    app_name: str = "Lotusette"
    debug: bool = False
    
    # LLM
    llm_provider: str = "openai"
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    
    # Database
    database_url: str
    vector_db_url: str
    
    # Voice
    stt_provider: str = "whisper"
    tts_provider: str = "coqui"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"
```

## Tests

```python
tests/
├── unit/                # Tests unitaires
│   ├── test_llm.py
│   ├── test_memory.py
│   └── ...
├── integration/         # Tests d'intégration
│   ├── test_api.py
│   ├── test_conversation.py
│   └── ...
├── e2e/                 # Tests end-to-end
│   └── test_full_flow.py
└── fixtures/            # Fixtures et mocks
    └── ...
```

## Déploiement

### Development
```bash
docker-compose up
```

### Production
- Docker containers
- Kubernetes orchestration
- CI/CD pipeline (GitHub Actions)
- Infrastructure as Code (Terraform)

---

Ce document évoluera avec le projet. Contributions et suggestions bienvenues !
