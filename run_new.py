"""
Ponto de entrada da aplicação Flask modularizada
Sistema de Previsão do Metrô de Fortaleza
"""

from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Configurações para desenvolvimento
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    port = int(os.environ.get("PORT", 5000))

    print("Sistema de Previsão do Metrô")
    print("=" * 50)
    print(f"Rodando em: http://localhost:{port}")
    print(f"Debug: {'Ativado' if debug_mode else 'Desativado'}")
    print(f"Admin: http://localhost:{port}/admin")
    print(f"API Docs: http://localhost:{port}/docs")
    print("=" * 50)

    app.run(host="0.0.0.0", port=port, debug=debug_mode)
