#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de inicialização do Sistema de Previsão do Metrô
Versão compatível com Windows usando Random Forest
"""

import sys
import os


def check_dependencies():
    """Verificar se todas as dependências estão instaladas"""
    required_packages = ["flask", "pandas", "numpy", "sklearn", "wtforms"]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"[OK] {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"[FALTA] {package}")

    if missing_packages:
        print(f"\nInstalando pacotes faltantes: {', '.join(missing_packages)}")
        for package in missing_packages:
            os.system(f"pip install {package}")

    return len(missing_packages) == 0


def initialize_system():
    """Inicializar o sistema"""
    print("Sistema de Previsão do Metrô - Metrofor")
    print("=" * 50)

    # Verificar dependências
    print("Verificando dependências...")
    if not check_dependencies():
        print("[ERRO] Erro ao instalar dependências")
        return False

    # Inicializar banco de dados
    print("\nInicializando banco de dados...")
    try:
        from database import init_db

        init_db()
        print("[OK] Banco de dados inicializado!")
    except Exception as e:
        print(f"[ERRO] Erro no banco de dados: {e}")
        return False

    # Inicializar modelo ML
    print("\nInicializando modelo de Machine Learning...")
    try:
        from ml_model import MetroPredictor

        predictor = MetroPredictor()
        print("[OK] Modelo ML inicializado!")

        # Mostrar informações do modelo
        info = predictor.get_model_info()
        print(f"   Tipo: {info['model_type']}")
        print(f"   Estações: {info['stations_count']}")
        print(f"   Treinado: {'Sim' if info['is_trained'] else 'Não'}")

    except Exception as e:
        print(f"[ERRO] Erro no modelo ML: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


def start_server():
    """Iniciar servidor Flask"""
    try:
        from app import app

        print("\nIniciando servidor Flask...")
        print("Acesse: http://localhost:5000")
        print("API Docs: http://localhost:5000/docs")
        print("\n[INFO] Pressione Ctrl+C para parar o servidor")
        print("=" * 50)

        app.run(debug=True, host="0.0.0.0", port=5000)

    except KeyboardInterrupt:
        print("\n\nServidor parado pelo usuário")
    except Exception as e:
        print(f"\n[ERRO] Erro ao iniciar servidor: {e}")
        import traceback

        traceback.print_exc()


def main():
    """Função principal"""
    try:
        # Adicionar diretório atual ao path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)

        # Inicializar sistema
        if initialize_system():
            # Iniciar servidor
            start_server()
        else:
            print("\n[ERRO] Falha na inicialização do sistema")
            input("Pressione Enter para sair...")

    except Exception as e:
        print(f"\n[ERRO] Erro crítico: {e}")
        import traceback

        traceback.print_exc()
        input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
