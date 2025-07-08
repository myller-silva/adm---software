from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import os
import json
import sys

# Adicionar o diretório pai ao path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SECRET_KEY, ADMIN_DATABASE, TEMPLATES_DIR, STATIC_DIR

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(
        __name__,
        template_folder=TEMPLATES_DIR,
        static_folder=STATIC_DIR,
    )

    # Configurações centralizadas
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{ADMIN_DATABASE}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Adicionar filtro personalizado para JSON
    @app.template_filter("from_json")
    def from_json_filter(value):
        if value:
            try:
                return json.loads(value)
            except:
                return []
        return []

    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "admin.login"
    login_manager.login_message = "Por favor, faça login para acessar esta página."

    # Registrar blueprints
    from app.blueprints.main import main_bp
    from app.blueprints.api import api_bp
    from app.blueprints.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Criar tabelas
    with app.app_context():
        from app.models.alert import Alert
        from app.models.user import User

        db.create_all()

        # Inicializar banco de dados de horários do metrô
        try:
            from database import init_db
            init_db()
        except Exception as e:
            print(f"Erro ao inicializar banco de dados de horários: {e}")

        # Criar usuário admin padrão se não existir
        if not User.query.filter_by(username="admin").first():
            admin_user = User(username="admin", email="admin@metrofor.ce.gov.br")
            admin_user.set_password("admin123")
            db.session.add(admin_user)
            db.session.commit()

        # Criar alguns alertas de exemplo se não existirem
        if Alert.query.count() == 0:
            sample_alerts = [
                # Alert(
                #     title="Horário de Funcionamento",
                #     message="O metrô funciona de segunda a sábado das 05:30 às 23:00.",
                #     type="info",
                #     priority="low",
                #     stations=None,
                #     active=True,
                # ),
                Alert(
                    title="Manutenção Programada",
                    message="Haverá manutenção na estação Parangaba no domingo das 06:00 às 12:00.",
                    type="warning",
                    priority="medium",
                    stations='["Parangaba"]',
                    active=True,
                ),
                Alert(
                    title="Velocidade Reduzida",
                    message="Trens operando em velocidade reduzida por motivos de segurança.",
                    type="warning",
                    priority="high",
                    stations=None,
                    active=True,
                ),
            ]

            for alert in sample_alerts:
                db.session.add(alert)
            db.session.commit()

    return app
