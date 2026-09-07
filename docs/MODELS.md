# Modèles LLM sélectionnés — Lotusette

Fiche de référence pour le choix du modèle local selon la machine. À lire avant toute
modification de `lotusette/core/llm/` ou de la configuration `LLM_PROVIDER`.

Dernière vérification : septembre 2026.

---

## Règle d'accès unique

Tous les modèles ci-dessous sont servis par `llama-server` (llama.cpp), qui expose une API
compatible OpenAI sur `/v1/chat/completions`.

Le provider est implémenté dans `lotusette/core/llm/local_openai_provider.py` et se
sélectionne avec `LLM_PROVIDER=local`. Il ne dépend d'aucune spécificité vLLM : le corps de
requête n'utilise que `model`, `messages`, `temperature`, `max_tokens` et `stream`.

Les noms `local-vllm`, `llamacpp` et `ollama` restent acceptés comme alias de `local`, et la
classe `LocalVLLMProvider` reste un alias de `LocalOpenAIProvider`.

`local_transformers_provider.py` a été supprimé. Il imposait `torch`, `transformers`,
`accelerate` et `bitsandbytes` pour un résultat plus lent que llama.cpp sur le même matériel.

---

## Modèle retenu par défaut : Ministral 3 Instruct

Éditeur `mistralai`, publié en 2512, licence Apache 2.0.

Retenu pour la boucle conversationnelle sur les trois machines. Justification :

- Non-raisonnant. Pas de bloc `<think>` avant la réponse, ce qui est indispensable pour la
  latence de la Phase 2 vocale.
- Function calling natif et sortie JSON. Répond directement au besoin de l'étape outils.
- Adhérence au prompt système mise en avant par l'éditeur. La personnalité de Lotusette
  repose entièrement sur `prompt_manager.py`, ce critère est structurant.
- GGUF publiés officiellement par `mistralai`, pas par un quantiseur tiers.
- Contexte natif 256k, encodeur vision de 0,4B inclus.
- Le français est une langue de premier plan, ce qui est un bonus et non un critère bloquant.

**Prendre la variante `Instruct`, jamais `Reasoning`.** Les deux existent en GGUF officiel
dans la même collection. La variante Reasoning génère une trace de raisonnement avant de
répondre : correct pour un calcul, rédhibitoire pour une conversation vocale.

---

## Sélection par machine

### PC portable — i5-10500H, RTX 3060 Laptop 6 Go

**Modèle : `mistralai/Ministral-3-3B-Instruct-2512-GGUF`, quant `Q4_K_M`.**

Le 8B en Q4_K_M pèse 5,2 Go. Il ne tient pas dans 6 Go une fois ajoutés le cache KV et
l'overhead CUDA. Ne pas l'utiliser sur cette machine en offload complet.

Repli acceptable si la qualité prime sur la latence : 8B Q4_K_M avec `-ngl 24` et le reste
sur CPU. Attendre 8 à 12 tok/s sur ce processeur en DDR4. Insuffisant pour la boucle vocale.

Machine à considérer comme un poste de développement et de test, pas comme une cible de
production.

### PC fixe — i7-13700K, RTX 4070 Ti 12 Go, 32 Go DDR5

**Modèle principal : `mistralai/Ministral-3-14B-Instruct-2512-GGUF`, quant `Q4_K_M`.**

| Poste | VRAM |
|---|---|
| Modèle Q4_K_M | 8,24 Go |
| `faster-whisper` large-v3-turbo | ~2 Go |
| Cache KV à 16k de contexte | ~1,5 Go |
| **Total** | **~11,8 Go sur 12** |

C'est serré mais tenable. Si ça déborde, descendre le contexte à 8k avant de changer de
quant. Le Q5_K_M à 9,62 Go ne laisse pas assez de marge pour Whisper.

**Modèle secondaire, expérimental : `ornith-ai/Ornith-1.5-35B-A3B-GGUF`, quant `Q4_K_M`.**

MoE de 35B avec ~3B activés par token, licence MIT, architecture `qwen35moe`. 21,7 Go, donc
hors VRAM, mais l'offload MoE le rend exploitable :

```bash
llama-server -hf ornith-ai/Ornith-1.5-35B-A3B-GGUF:Q4_K_M \
  --n-cpu-moe 30 -c 16384 --port 8081
```

**Contrainte dure : avec 32 Go de RAM, les deux modèles ne peuvent pas être chargés
simultanément.** L'architecture à deux modèles est reportée au serveur. Sur cette machine,
c'est un modèle à la fois, éventuellement via `llama-swap` pour les tâches de fond.

Ornith est un modèle de raisonnement avec bloc `<think>` par défaut, et ses benchmarks sont
exclusivement orientés code et agentique. Ne pas le mettre sur la boucle conversationnelle.

### Serveur — matériel non arrêté

Architecture cible à deux modèles, deux instances `llama-server` sur deux ports, routage par
type de tâche dans `agent.py`.

| Rôle | Modèle | Quant | Poids |
|---|---|---|---|
| Conversation, port 8080 | Ministral 3 14B Instruct | Q5_K_M | 9,62 Go |
| Agent et tâches de fond, port 8081 | Ornith-1.5-35B-A3B | Q4_K_M | 21,7 Go |

Cible matérielle : 32 Go de VRAM minimum, 48 Go confortable. Prévoir 2 Go supplémentaires
pour Whisper résident.

La couche agent traite l'extraction des faits utilisateur, les résumés glissants, la
planification d'outils et la recherche web multi-étapes. Ces tâches sont insensibles à la
latence, le bloc `<think>` d'Ornith y devient un atout.

Alternative à évaluer pour la conversation si le multilingue devient prioritaire :
`Qwen/Qwen3.8-27B`, dense, Q4_K_M autour de 16,8 Go. Mode réflexion actif par défaut, à
désactiver.

Alternative pour la couche agent sur une machine à forte bande passante mémoire :
`mistralai/Mistral-Small-4-119B-2603`, MoE 119B avec 6,5B activés, effort de raisonnement
réglable par requête. Q4_K_M autour de 72 Go. À réserver à une plateforme 8 canaux
(Threadripper ou EPYC). Sur du double canal grand public, la bande passante annule l'intérêt
de l'architecture.

---

## Configuration

### `.env` — PC fixe

```
LLM_PROVIDER=local
LOCAL_LLM_BASE_URL=http://localhost:8080/v1
LOCAL_LLM_MODEL=mistralai/Ministral-3-14B-Instruct-2512-GGUF:Q4_K_M
LOCAL_LLM_API_KEY=EMPTY
```

### `.env` — PC portable

```
LLM_PROVIDER=local
LOCAL_LLM_BASE_URL=http://localhost:8080/v1
LOCAL_LLM_MODEL=mistralai/Ministral-3-3B-Instruct-2512-GGUF:Q4_K_M
LOCAL_LLM_API_KEY=EMPTY
```

### Lancement du serveur d'inférence

```bash
# PC fixe
llama-server -hf mistralai/Ministral-3-14B-Instruct-2512-GGUF:Q4_K_M \
  -c 16384 --port 8080 --host 127.0.0.1

# PC portable
llama-server -hf mistralai/Ministral-3-3B-Instruct-2512-GGUF:Q4_K_M \
  -c 8192 --port 8080 --host 127.0.0.1
```

`llama-server` télécharge directement depuis Hugging Face avec `-hf`. Aucun téléchargement
manuel nécessaire.

### Politique de température

Mistral recommande de rester sous 0,1 pour le suivi d'instructions précis, et monte à 0,7
pour les tâches créatives. Ces deux régimes correspondent à deux usages distincts dans
Lotusette :

- Boucle d'outils active, extraction de faits, génération JSON : `temperature=0.1`
- Conversation libre, où la personnalité compte : `temperature=0.6` à `0.8`

`LLM_TEMPERATURE` fixe pour l'instant une valeur globale (0.7 par défaut). Le pilotage par
appel reste à faire : il deviendra nécessaire à l'étape E5, quand la boucle d'outils aura
besoin de 0.1 sans dégrader la conversation.

Pour Ornith, l'éditeur recommande `temperature=0.6`, `top_p=0.95`, `top_k=20`.

---

## À ne pas faire

- Ne pas laisser `-c` à sa valeur par défaut. Ces modèles annoncent 256k de contexte, ce qui
  ferait exploser l'allocation de cache KV. Plafonner à 8k ou 16k.
- Ne pas utiliser les variantes `Reasoning` ni Ornith sur la boucle conversationnelle.
- Ne pas utiliser les quantifications communautaires `abliterated` ou `uncensored` qui
  dominent le classement de tendance Hugging Face. Elles retirent les garde-fous du modèle,
  ce qui est un risque direct si Lotusette est un jour diffusée publiquement.
- Ne pas réintroduire `torch`, `transformers` ou `bitsandbytes` dans les dépendances.
- Ne pas oublier de réserver la VRAM de `faster-whisper` dans le calcul. Le modèle STT doit
  rester chargé en permanence, sinon chaque prise de parole coûte plusieurs secondes de
  rechargement.

---

## Chiffres vérifiés

Relevés sur les fiches modèles Hugging Face officielles.

| Modèle | Q4_K_M | Q5_K_M | Q6_K | Q8_0 |
|---|---|---|---|---|
| Ministral 3 14B Instruct | 8,24 Go | 9,62 Go | — | 14,4 Go |
| Ministral 3 8B Instruct | 5,2 Go | 6,06 Go | — | 9,03 Go |
| Ornith-1.5-35B-A3B | 21,7 Go | 25,3 Go | 29,2 Go | 37,8 Go |

Ministral 3 14B se compose de 13,5B pour le modèle de langage et 0,4B pour l'encodeur vision.
La version 8B se décompose en 8,4B et 0,4B.

---

## Estimations non mesurées

À traiter comme des ordres de grandeur, pas comme des mesures. Un script de benchmark doit
être écrit à l'étape E1 pour les remplacer par des valeurs réelles.

| Configuration | Débit estimé |
|---|---|
| 4070 Ti, Ministral 3 14B Q4_K_M, tout en VRAM | 35-50 tok/s |
| 4070 Ti + 32 Go DDR5, Ornith Q4_K_M, `--n-cpu-moe` | 15-25 tok/s |
| 3060 Laptop, Ministral 3 3B Q4_K_M, tout en VRAM | 40-60 tok/s |
| 3060 Laptop, Ministral 3 8B Q4_K_M, offload partiel | 8-12 tok/s |

Seuil de confort pour la conversation vocale : 25 tok/s soutenus et premier token sous
400 ms.

---

## À vérifier avant de figer

- Taille exacte des GGUF de `Ministral-3-3B-Instruct-2512-GGUF`, non relevée. L'estimation
  de 2 Go en Q4_K_M reste à confirmer sur la fiche modèle.
- Licence et taille exacte de `Qwen/Qwen3.8-27B`, non confirmées.
- Licence de `Mistral-Small-4-119B-2603`, non confirmée.
- Possibilité de désactiver le mode réflexion d'Ornith-1.5 via le gabarit de conversation.
  Le modèle a été entraîné par apprentissage par renforcement avec la réflexion active, la
  désactiver pourrait dégrader ses performances.
~~Compatibilité du corps de requête avec llama.cpp.~~ Vérifié : le provider n'envoie que
des champs standards de l'API OpenAI, et l'en-tête `Authorization: Bearer EMPTY` est
toujours présent et bien formé. Un test unitaire verrouille ce contrat
(`tests/unit/test_local_openai_provider.py::TestRequestPayload`).
