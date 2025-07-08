from flask import Blueprint, jsonify, request
from app.models.alert import Alert
from app.utils.timezone import get_region_time
from datetime import datetime
import sys
import os

# Adicionar o diretório raiz ao path para importar módulos antigos
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from database import get_scheduled_times, save_real_time_update
from ml_model import MetroPredictor

api_bp = Blueprint("api", __name__)

# Lista de estações
STATIONS = [
    "Chico da Silva",
    "J.Alencar",
    "S.Benedito",
    "Benfica",
    "Pe.Cicero",
    "Porangabussu",
    "C.Fernandes",
    "J.kubitschek",
    "Parangaba",
    "V.Pery",
    "M.Satiro",
    "Mondubim",
    "Esperanca",
    "Aracape",
    "A.Alegre",
    "R.Queiroz",
    "V.Tavora",
    "Maracanaú",
    "Jereissati",
    "C. Benevides",
]

# Carregar modelo de ML
predictor = MetroPredictor()


@api_bp.route("/alertas")
def api_alertas():
    """API para obter alertas atuais"""
    try:
        alerts = [alert.to_dict() for alert in Alert.get_active_alerts()]
        return jsonify(
            {
                "status": "success",
                "alerts": alerts,
                "total": len(alerts),
                "timestamp": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@api_bp.route("/horarios/<station>/<direction>")
def api_horarios(station, direction):
    """API endpoint para consultar horários"""
    try:
        scheduled_times = get_scheduled_times(station, direction)
        current_time = get_region_time().time()
        next_trains = []

        for time_str in scheduled_times:
            train_time = datetime.strptime(time_str, "%H:%M").time()
            if train_time > current_time:
                predicted_time = predictor.predict_arrival_time(
                    station, direction, time_str, get_region_time()
                )
                next_trains.append(
                    {
                        "scheduled": time_str,
                        "predicted": predicted_time.strftime("%H:%M"),
                        "delay_minutes": int(
                            (
                                predicted_time
                                - datetime.combine(get_region_time().date(), train_time)
                            ).total_seconds()
                            / 60
                        ),
                    }
                )
                if len(next_trains) >= 5:
                    break

        return jsonify(
            {
                "status": "success",
                "station": station,
                "direction": direction,
                "trains": next_trains,
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@api_bp.route("/report", methods=["POST"])
def api_report():
    """API endpoint para reportar horários reais"""
    try:
        data = request.get_json()
        station = data.get("station")
        direction = data.get("direction")
        actual_time_str = data.get("actual_time")

        if not all([station, direction, actual_time_str]):
            return jsonify({"status": "error", "message": "Dados incompletos"}), 400

        actual_time = datetime.fromisoformat(actual_time_str)

        # Validar estação
        if station not in STATIONS:
            return jsonify({"status": "error", "message": "Estação inválida"}), 400

        # Salvar no banco
        save_real_time_update(station, direction, actual_time)

        # Atualizar modelo
        predictor.update_model(station, direction, actual_time)

        return jsonify(
            {"status": "success", "message": "Horário reportado com sucesso"}
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
