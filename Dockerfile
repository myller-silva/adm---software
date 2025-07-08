# Use uma imagem Python oficial como base
FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run_new.py
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV PORT=5000

# Criar diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de requisitos primeiro (para melhor cache)
COPY requirements.txt .

# Atualizar pip e instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip==23.3.1 && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos do projeto
COPY . .

# Criar diretórios necessários
RUN mkdir -p /app/data && \
    mkdir -p /app/database && \
    mkdir -p /app/models && \
    mkdir -p /app/static && \
    mkdir -p /app/templates

# Definir permissões adequadas
RUN chmod +x run_new.py

# Expor a porta da aplicação
EXPOSE 5000

# Comando de saúde para verificar se o container está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Comando para executar a aplicação diretamente
CMD ["python", "run_new.py"]
