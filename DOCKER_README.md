# Docker Setup - Sistema de Previsão do Metrô

Este documento explica como executar o projeto usando Docker.

## Pré-requisitos

- Docker instalado
- Docker Compose instalado (opcional, mas recomendado)

## Opção 1: Usando Docker Compose (Recomendado)

### Construir e executar o container

```bash
docker-compose up --build
```

### Executar em segundo plano

```bash
docker-compose up -d --build
```

### Parar o container

```bash
docker-compose down
```

### Ver logs

```bash
docker-compose logs -f
```

## Opção 2: Usando Docker diretamente

### Construir a imagem

```bash
docker build -t metro-prediction-app .
```

### Executar o container

```bash
docker run -d \
  --name metro-app \
  -p 5000:5000 \
  -v "$(pwd)/data:/app/data" \
  metro-prediction-app
```

### Parar o container

```bash
docker stop metro-app
docker rm metro-app
```

## Acessar a aplicação

Após executar o container, acesse:

- **URL**: <http://localhost:5000>
- **Documentação da API**: <http://localhost:5000/docs>

## Comandos úteis

### Ver containers em execução

```bash
docker ps
```

### Ver logs do container

```bash
docker logs metro-app
```

### Acessar o terminal do container

```bash
docker exec -it metro-app bash
```

### Limpar imagens não utilizadas

```bash
docker system prune -a
```

## Volumes

- `./data:/app/data` - Persistência dos dados do banco de dados
- `./logs:/app/logs` - Logs da aplicação (opcional)

## Variáveis de ambiente

O container utiliza as seguintes variáveis de ambiente:

- `FLASK_ENV=production`
- `FLASK_APP=app.py`
- `PYTHONDONTWRITEBYTECODE=1`
- `PYTHONUNBUFFERED=1`

## Troubleshooting

### Container não inicia

1. Verifique os logs: `docker-compose logs`
2. Verifique se a porta 5000 não está em uso
3. Verifique se o Docker tem permissões adequadas

### Dados não persistem

1. Certifique-se que o diretório `./data` existe
2. Verifique as permissões do diretório

### Performance lenta

1. Aloque mais recursos ao Docker
2. Considere usar uma imagem base mais leve se necessário
