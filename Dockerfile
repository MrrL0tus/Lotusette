# Lotusette — image de commodité.
#
# Docker avait été introduit pour contourner une dépendance (Coqui TTS) qui
# imposait Python < 3.12. Cette dépendance a été retirée : l'installation
# locale fonctionne sur toutes les versions supportées, et cette image n'est
# plus qu'une commodité.
#
# Le modèle ne tourne PAS dans ce conteneur : Lotusette parle à un serveur
# llama.cpp ou Ollama sur l'hôte. Voir docs/MODELS.md.

FROM python:3.13-slim

WORKDIR /app

# Copier d'abord les dépendances, pour profiter du cache de couches.
COPY requirements.txt pyproject.toml ./

RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --no-cache-dir --no-deps -e .

# Les données vivent hors du package et sont montées en volume.
ENV PYTHONUNBUFFERED=1 \
    LOTUSETTE_DATA_DIR=/data

# Le serveur d'inférence tourne sur l'hôte, pas ici.
ENV LOCAL_LLM_BASE_URL=http://host.docker.internal:8080/v1

# 8000 : API FastAPI (étape E7, pas encore implémentée)
EXPOSE 8000

CMD ["python", "-m", "lotusette.ui.cli"]
