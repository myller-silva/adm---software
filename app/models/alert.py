from app import db
from datetime import datetime


class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(
        db.String(20), nullable=False, default="info"
    )  # danger, warning, info
    priority = db.Column(
        db.String(20), nullable=False, default="low"
    )  # high, medium, low
    stations = db.Column(db.Text)  # JSON string com lista de estações afetadas
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Alert {self.title}>"

    def to_dict(self):
        import json

        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "type": self.type,
            "priority": self.priority,
            "stations": json.loads(self.stations) if self.stations else None,
            "active": self.active,
            "timestamp": self.created_at,
        }

    @staticmethod
    def get_active_alerts():
        """Retorna todos os alertas ativos"""
        return (
            Alert.query.filter_by(active=True).order_by(Alert.created_at.desc()).all()
        )

    @staticmethod
    def get_high_priority_alerts():
        """Retorna alertas de alta prioridade para a página inicial"""
        return (
            Alert.query.filter_by(active=True, priority="high")
            .order_by(Alert.created_at.desc())
            .limit(3)
            .all()
        )
