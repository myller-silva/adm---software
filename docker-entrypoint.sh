#!/bin/bash

# Script de inicialização para o container Docker

echo "Iniciando aplicação Metro..."

# Verificar se todos os arquivos críticos estão presentes
echo "Verificando arquivos críticos..."

# Verificar arquivos de dados
if [ ! -f "data/horarios_metro_ida.csv" ]; then
    echo "ERRO: Arquivo data/horarios_metro_ida.csv não encontrado!"
    exit 1
fi

if [ ! -f "data/horarios_metro_volta.csv" ]; then
    echo "ERRO: Arquivo data/horarios_metro_volta.csv não encontrado!"
    exit 1
fi

# Verificar arquivos de modelo ML
if [ ! -f "models/metro_model.pkl" ]; then
    echo "ERRO: Arquivo models/metro_model.pkl não encontrado!"
    exit 1
fi

if [ ! -f "models/encoders.pkl" ]; then
    echo "ERRO: Arquivo models/encoders.pkl não encontrado!"
    exit 1
fi

if [ ! -f "models/scaler.pkl" ]; then
    echo "ERRO: Arquivo models/scaler.pkl não encontrado!"
    exit 1
fi

# Verificar arquivos de database
if [ ! -f "database/metro_admin.db" ]; then
    echo "AVISO: Arquivo database/metro_admin.db não encontrado. Será criado na primeira execução."
fi

if [ ! -f "database/metro_database.db" ]; then
    echo "AVISO: Arquivo database/metro_database.db não encontrado. Será criado na primeira execução."
fi

echo "Verificação completa! Todos os arquivos críticos estão presentes."

# Garantir permissões corretas
chmod 644 data/*.csv 2>/dev/null || true
chmod 644 models/*.pkl 2>/dev/null || true
chmod 666 database/*.db 2>/dev/null || true

# Executar a aplicação
echo "Iniciando aplicação Flask..."
exec python run_new.py
