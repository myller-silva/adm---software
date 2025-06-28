# Use uma imagem Python oficial como base
FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Criar diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de requisitos
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos do projeto
COPY . .

# Criar diretório para dados persistentes
RUN mkdir -p /app/data

# Definir permissões adequadas
RUN chmod +x start.py run.py

# Inicializar o banco de dados
RUN python -c "from database import init_db; init_db()"

# Expor a porta da aplicação
EXPOSE 5000

# Comando de saúde para verificar se o container está funcionando
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Comando para executar a aplicação
CMD ["python", "app.py"]
