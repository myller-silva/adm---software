"""
Script simples para iniciar o aplicativo Flask modular
"""
import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app

    if __name__ == "__main__":
        app = create_app()
        print("Iniciando servidor Flask modular...")
        print("Admin: http://localhost:5000/admin")
        print("Site: http://localhost:5000")
        app.run(debug=True, host="0.0.0.0", port=5000)

except ImportError as e:
    print(f"Erro de importação: {e}")
    print("Instalando dependências...")
    os.system("pip install flask flask-sqlalchemy flask-login flask-wtf wtforms")
    print("Tente executar novamente")
except Exception as e:
    print(f"Erro: {e}")
    sys.exit(1)
