# Use uma imagem Python oficial como base
FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

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

# Criar diretório para dados persistentes
RUN mkdir -p /app/data

# Definir permissões adequadas
RUN chmod +x start.py run.py

# Expor a porta da aplicação
EXPOSE 5000

# Comando de saúde para verificar se o container está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Script de inicialização que configura o banco e inicia a aplicação
RUN echo '#!/bin/bash\nset -e\necho "Inicializando banco de dados..."\npython -c "from database import init_db; init_db()"\necho "Banco de dados inicializado com sucesso!"\necho "Iniciando aplicação Flask..."\nexec python app.py' > /app/start.sh && \
    chmod +x /app/start.sh

# Comando para executar a aplicação
CMD ["/app/start.sh"]
