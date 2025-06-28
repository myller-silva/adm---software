# Script PowerShell para gerenciar o Docker do Sistema de Previsão do Metrô

param(
    [string]$Action
)

Write-Host "=== Sistema de Previsão do Metrô - Docker Manager ===" -ForegroundColor Cyan
Write-Host ""

switch ($Action) {
    "build" {
        Write-Host "Construindo a imagem Docker..." -ForegroundColor Yellow
        docker build -t metro-prediction-app .
    }
    "start" {
        Write-Host "Iniciando o container..." -ForegroundColor Green
        docker-compose up -d --build
        Write-Host "Aplicação disponível em: http://localhost:5000" -ForegroundColor Green
    }
    "stop" {
        Write-Host "Parando o container..." -ForegroundColor Red
        docker-compose down
    }
    "logs" {
        Write-Host "Exibindo logs..." -ForegroundColor Blue
        docker-compose logs -f
    }
    "restart" {
        Write-Host "Reiniciando o container..." -ForegroundColor Yellow
        docker-compose down
        docker-compose up -d --build
        Write-Host "Aplicação reiniciada: http://localhost:5000" -ForegroundColor Green
    }
    "clean" {
        Write-Host "Limpando containers e imagens..." -ForegroundColor Magenta
        docker-compose down
        try {
            docker rmi metro-prediction-app
        } catch {
            # Ignora erro se a imagem não existir
        }
        docker system prune -f
    }
    "status" {
        Write-Host "Status dos containers:" -ForegroundColor Blue
        docker ps --filter "name=metro"
    }
    default {
        Write-Host "Uso: .\docker.ps1 {build|start|stop|logs|restart|clean|status}" -ForegroundColor Red
        Write-Host ""
        Write-Host "Comandos disponíveis:" -ForegroundColor White
        Write-Host "  build   - Constrói a imagem Docker" -ForegroundColor Gray
        Write-Host "  start   - Inicia a aplicação" -ForegroundColor Gray
        Write-Host "  stop    - Para a aplicação" -ForegroundColor Gray
        Write-Host "  logs    - Exibe os logs" -ForegroundColor Gray
        Write-Host "  restart - Reinicia a aplicação" -ForegroundColor Gray
        Write-Host "  clean   - Remove containers e imagens" -ForegroundColor Gray
        Write-Host "  status  - Mostra status dos containers" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Exemplo: .\docker.ps1 start" -ForegroundColor Yellow
        exit 1
    }
}
