#!/bin/bash
# Script helper pour Docker - Construction et démarrage

set -euo pipefail

echo "🚀 Lotusette Docker Helper"
echo "=========================="
echo ""

# Fonction d'aide
show_help() {
    echo "Usage: ./docker-helper.sh [command]"
    echo ""
    echo "Commands:"
    echo "  build       - Construire l'image Docker"
    echo "  start       - Démarrer tous les services"
    echo "  stop        - Arrêter tous les services"
    echo "  restart     - Redémarrer tous les services"
    echo "  cli         - Lancer l'interface CLI interactive"
    echo "  api         - Lancer le serveur API"
    echo "  logs        - Voir les logs"
    echo "  shell       - Ouvrir un shell dans le container"
    echo "  clean       - Nettoyer les containers et volumes"
    echo "  help        - Afficher cette aide"
    echo ""
}

# Vérifier que docker et docker-compose sont installés
check_dependencies() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord."
        exit 1
    fi
}

# Déterminer la commande docker compose
get_compose_cmd() {
    if docker compose version &> /dev/null; then
        echo "docker compose"
    else
        echo "docker-compose"
    fi
}

check_dependencies
COMPOSE_CMD=$(get_compose_cmd)

case "${1:-help}" in
    build)
        echo "📦 Construction de l'image Docker..."
        $COMPOSE_CMD build
        echo "✅ Image construite avec succès!"
        ;;
    
    start)
        echo "🚀 Démarrage des services..."
        $COMPOSE_CMD up -d postgres redis
        echo "⏳ Attente que les services soient prêts..."
        sleep 5
        echo "✅ Services démarrés!"
        echo ""
        echo "Pour lancer l'interface CLI: ./docker-helper.sh cli"
        echo "Pour lancer l'API: ./docker-helper.sh api"
        ;;
    
    stop)
        echo "🛑 Arrêt des services..."
        $COMPOSE_CMD down
        echo "✅ Services arrêtés!"
        ;;
    
    restart)
        echo "🔄 Redémarrage des services..."
        $COMPOSE_CMD restart
        echo "✅ Services redémarrés!"
        ;;
    
    cli)
        echo "💬 Lancement de l'interface CLI..."
        $COMPOSE_CMD run --rm lotusette python -m lotusette.ui.cli
        ;;
    
    api)
        echo "🌐 Lancement du serveur API..."
        $COMPOSE_CMD up lotusette
        ;;
    
    logs)
        echo "📋 Logs des services..."
        $COMPOSE_CMD logs -f
        ;;
    
    shell)
        echo "🐚 Ouverture d'un shell dans le container..."
        $COMPOSE_CMD run --rm lotusette /bin/bash
        ;;
    
    clean)
        echo "🧹 Nettoyage des containers et volumes..."
        read -p "⚠️  Cela supprimera tous les données! Continuer? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            $COMPOSE_CMD down -v
            echo "✅ Nettoyage terminé!"
        else
            echo "❌ Annulé."
        fi
        ;;
    
    help|--help|-h)
        show_help
        ;;
    
    *)
        echo "❌ Commande inconnue: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
