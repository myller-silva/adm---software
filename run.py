#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app

    print("Aplicação importada com sucesso!")

    # Testar inicialização do banco
    from database import init_db

    init_db()
    print("Banco de dados inicializado!")

    # Testar modelo ML
    from ml_model import MetroPredictor

    predictor = MetroPredictor()
    print("Modelo de ML inicializado!")

    # Executar aplicação
    print("Iniciando servidor Flask...")
    app.run(debug=True, host="0.0.0.0", port=5000)

except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Instalando dependências...")
    os.system(
        "pip install flask pandas numpy tensorflow scikit-learn wtforms flask-wtf"
    )

except Exception as e:
    print(f"Erro geral: {e}")
    import traceback

    traceback.print_exc()
