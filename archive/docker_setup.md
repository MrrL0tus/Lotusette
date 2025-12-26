# Guide Docker pour Lotusette

## 📋 Vue d'ensemble

Ce guide explique comment utiliser Docker avec Lotusette pour garantir la bonne version de Python et éviter les problèmes de compatibilité.

## ❓ Pourquoi Docker ?

### Problème résolu
- **Issue #3**: Python 3.13 n'est pas compatible avec TTS (Text-to-Speech)
- TTS nécessite Python < 3.12
- Docker force l'utilisation de Python 3.11, garantissant la compatibilité avec **toutes** les dépendances

### Avantages de Docker
1. ✅ **Version Python garantie**: Python 3.11 automatiquement
2. ✅ **Environnement isolé**: Pas de conflits avec votre système
3. ✅ **Reproductibilité**: Fonctionne de la même manière partout
4. ✅ **Services intégrés**: PostgreSQL et Redis inclus
5. ✅ **Déploiement facile**: Prêt pour la production

## 📦 Installation

### Prérequis
- [Docker](https://docs.docker.com/get-docker/) (version 20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0+)

### Vérification
```bash
docker --version
docker-compose --version
```

## 🚀 Démarrage rapide

### 1. Configuration initiale

```bash
# Cloner le dépôt (si pas déjà fait)
git clone https://github.com/MrrL0tus/Lotusette.git
cd Lotusette

# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env avec vos clés API (si nécessaire)
nano .env
```

### 2. Utilisation du script helper

Le script `docker-helper.sh` simplifie l'utilisation de Docker:

```bash
# Rendre le script exécutable
chmod +x docker-helper.sh

# Voir toutes les commandes disponibles
./docker-helper.sh help
```

### 3. Construction et démarrage

```bash
# Construire l'image Docker
./docker-helper.sh build

# Démarrer les services (PostgreSQL, Redis)
./docker-helper.sh start

# Lancer l'interface CLI
./docker-helper.sh cli
```

## 📚 Commandes disponibles

### Construction
```bash
# Construire ou reconstruire l'image
./docker-helper.sh build
```

### Gestion des services
```bash
# Démarrer tous les services en arrière-plan
./docker-helper.sh start

# Arrêter tous les services
./docker-helper.sh stop

# Redémarrer tous les services
./docker-helper.sh restart
```

### Utilisation
```bash
# Lancer l'interface CLI interactive
./docker-helper.sh cli

# Lancer le serveur API (futur)
./docker-helper.sh api

# Voir les logs des services
./docker-helper.sh logs

# Ouvrir un shell dans le container
./docker-helper.sh shell
```

### Nettoyage
```bash
# Supprimer containers et volumes (⚠️ supprime les données!)
./docker-helper.sh clean
```

## 🔧 Utilisation avancée

### Docker Compose manuel

Si vous préférez utiliser directement docker-compose:

```bash
# Construire
docker-compose build

# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

### Exécuter des commandes dans le container

```bash
# Lancer une commande ponctuelle
docker-compose run --rm lotusette python -c "print('Hello from Docker!')"

# Installer des dépendances supplémentaires
docker-compose run --rm lotusette pip install nouvelle-bibliotheque

# Lancer les tests
docker-compose run --rm lotusette pytest
```

### Volumes et persistance

Docker Compose configure automatiquement 3 volumes:
- `lotusette-data`: Données de l'application et modèles
- `postgres-data`: Base de données PostgreSQL
- `redis-data`: Cache Redis

Ces volumes persistent les données entre les redémarrages.

## 🐛 Dépannage

### Le build échoue
```bash
# Nettoyer et reconstruire from scratch
docker-compose down -v
docker-compose build --no-cache
```

### Port déjà utilisé
Si le port 8000, 5432 ou 6379 est déjà utilisé:
```bash
# Éditer docker-compose.yml et changer les ports
# Par exemple: "8001:8000" au lieu de "8000:8000"
```

### Problème de permissions
```bash
# Sur Linux, si vous avez des problèmes de permissions:
sudo chown -R $USER:$USER .
```

### Logs pour déboguer
```bash
# Voir tous les logs
./docker-helper.sh logs

# Voir les logs d'un service spécifique
docker-compose logs lotusette
docker-compose logs postgres
```

## 📁 Structure des fichiers Docker

```
Lotusette/
├── Dockerfile              # Définition de l'image Docker
├── docker-compose.yml      # Orchestration des services
├── .dockerignore          # Fichiers à exclure du build
└── docker-helper.sh       # Script helper pour faciliter l'usage
```

## 🔐 Sécurité

### En développement
- Les ports sont exposés sur localhost uniquement
- Utilisez des mots de passe forts dans `.env`
- Ne commitez JAMAIS le fichier `.env`

### En production
- Changez TOUS les mots de passe par défaut
- Utilisez des secrets Docker
- Configurez un reverse proxy (nginx)
- Activez HTTPS

## 🎯 Prochaines étapes

1. ✅ Docker configuré avec Python 3.11
2. 📖 Consultez [local_models_guide.md](local_models_guide.md) pour les modèles locaux
3. 🚀 Consultez [getting_started_ai.md](getting_started_ai.md) pour créer votre IA

## 🆘 Besoin d'aide ?

- 📚 [Documentation Docker](https://docs.docker.com/)
- 📚 [Documentation Docker Compose](https://docs.docker.com/compose/)
- 🐛 [Ouvrir une issue](https://github.com/MrrL0tus/Lotusette/issues)

---

**Date de création**: 2025-12-26  
**Dernière mise à jour**: 2025-12-26  
**Version Docker**: Python 3.11-slim
