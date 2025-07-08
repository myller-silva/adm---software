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

# Copiar arquivos críticos primeiro (modelos e dados)
COPY data/ ./data/
COPY models/ ./models/
COPY database/ ./database/

# Copiar código da aplicação
COPY app/ ./app/
COPY templates/ ./templates/
COPY static/ ./static/

# Copiar arquivos de configuração e execução
COPY config.py ml_model.py database.py run_new.py ./
COPY docker-entrypoint.sh ./

# Verificar se arquivos críticos estão presentes
RUN echo "Verificando arquivos críticos..." && \
    ls -la data/ && \
    ls -la models/ && \
    ls -la database/ && \
    if [ ! -f "data/horarios_metro_ida.csv" ] || [ ! -f "data/horarios_metro_volta.csv" ]; then \
        echo "ERRO: Arquivos CSV de horários não encontrados!"; \
        exit 1; \
    fi && \
    if [ ! -f "models/metro_model.pkl" ] || [ ! -f "models/encoders.pkl" ] || [ ! -f "models/scaler.pkl" ]; then \
        echo "ERRO: Arquivos de modelo ML não encontrados!"; \
        exit 1; \
    fi && \
    echo "Todos os arquivos críticos estão presentes!"

# Criar diretórios necessários se não existirem
RUN mkdir -p /app/data && \
    mkdir -p /app/database && \
    mkdir -p /app/models && \
    mkdir -p /app/static && \
    mkdir -p /app/templates

# Definir permissões adequadas para arquivos críticos
RUN chmod 644 data/*.csv && \
    chmod 644 models/*.pkl && \
    chmod 666 database/*.db || true && \
    chmod +x docker-entrypoint.sh && \
    chmod +x run_new.py

# Expor a porta da aplicação
EXPOSE 5000

# Comando de saúde para verificar se o container está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Comando para executar a aplicação com script de inicialização
CMD ["./docker-entrypoint.sh"]
