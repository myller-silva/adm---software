#!/bin/bash

# Script para facilitar o uso do Docker com o Sistema de Previsão do Metrô

echo "=== Sistema de Previsão do Metrô - Docker Manager ==="
echo ""

case "$1" in
    "build")
        echo "Construindo a imagem Docker..."
        docker build -t metro-prediction-app .
        ;;
    "start")
        echo "Iniciando o container..."
        docker-compose up -d --build
        echo "Aplicação disponível em: http://localhost:5000"
        ;;
    "stop")
        echo "Parando o container..."
        docker-compose down
        ;;
    "logs")
        echo "Exibindo logs..."
        docker-compose logs -f
        ;;
    "restart")
        echo "Reiniciando o container..."
        docker-compose down
        docker-compose up -d --build
        echo "Aplicação reiniciada: http://localhost:5000"
        ;;
    "clean")
        echo "Limpando containers e imagens..."
        docker-compose down
        docker rmi metro-prediction-app 2>/dev/null || true
        docker system prune -f
        ;;
    "status")
        echo "Status dos containers:"
        docker ps --filter "name=metro"
        ;;
    *)
        echo "Uso: $0 {build|start|stop|logs|restart|clean|status}"
        echo ""
        echo "Comandos disponíveis:"
        echo "  build   - Constrói a imagem Docker"
        echo "  start   - Inicia a aplicação"
        echo "  stop    - Para a aplicação"
        echo "  logs    - Exibe os logs"
        echo "  restart - Reinicia a aplicação"
        echo "  clean   - Remove containers e imagens"
        echo "  status  - Mostra status dos containers"
        echo ""
        echo "Exemplo: $0 start"
        exit 1
        ;;
esac
