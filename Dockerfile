# Lotusette - Dockerfile
# Force l'utilisation de Python 3.11 pour compatibilité avec toutes les dépendances
# Note: TTS nécessite Python <3.12, d'où le choix de Python 3.11

FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    ffmpeg \
    libsndfile1 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY requirements.txt requirements-dev.txt ./
COPY pyproject.toml ./

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Installer le package en mode développement
RUN pip install -e .

# Créer les répertoires pour les données et modèles
RUN mkdir -p /app/data/models /app/data/cache /app/data/db

# Exposer les ports
# 8000: API FastAPI
# 8080: Interface Web (future)
EXPOSE 8000 8080

# Variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1 \
    LOTUSETTE_DATA_DIR=/app/data \
    LOTUSETTE_MODELS_DIR=/app/data/models \
    LOTUSETTE_CACHE_DIR=/app/data/cache

# Commande par défaut (CLI)
CMD ["python", "-m", "lotusette.ui.cli"]
