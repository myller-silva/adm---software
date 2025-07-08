from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.forms.forms import StationForm, RealTimeForm
from app.models.alert import Alert
from app.utils.timezone import get_region_time
from datetime import datetime, timedelta
import sys
import os

# Adicionar o diretório raiz ao path para importar módulos antigos
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from database import get_scheduled_times, save_real_time_update, get_schedule_info
from ml_model import MetroPredictor

main_bp = Blueprint("main", __name__)

# Carregar modelo de ML
predictor = MetroPredictor()


@main_bp.route("/")
def index():
    form = StationForm()
    # Filtrar apenas alertas de alta prioridade para a página inicial
    alerts = [alert.to_dict() for alert in Alert.get_high_priority_alerts()]
    return render_template("index.html", form=form, alerts=alerts)


@main_bp.route("/consultar", methods=["POST"])
def consultar_horarios():
    form = StationForm()
    if form.validate_on_submit():
        station = form.station.data
        direction = form.direction.data

        # Mapear valores do formulário para nomes das direções no banco
        direction_mapping = {"ida": "Carlito Benevides", "volta": "Chico da Silva"}

        # Converter direção do formulário para direção do banco
        db_direction = direction_mapping.get(direction, direction)

        # Obter horários programados
        scheduled_times = get_scheduled_times(station, db_direction)
        current_time = get_region_time().time()
        next_trains = []

        for time_str in scheduled_times:
            train_time = datetime.strptime(time_str, "%H:%M").time()
            if train_time > current_time:
                predicted_time = predictor.predict_arrival_time(
                    station, db_direction, time_str, get_region_time()
                )
                next_trains.append(
                    {
                        "scheduled": time_str,
                        "predicted": predicted_time.strftime("%H:%M"),
                        "delay": int(
                            (
                                predicted_time
                                - datetime.combine(get_region_time().date(), train_time)
                            ).total_seconds()
                            / 60
                        ),
                    }
                )
                if len(next_trains) >= 3:  # Mostrar apenas os próximos 3 trens
                    break

        # Criar um novo formulário para a página de resultados
        new_form = StationForm()
        new_form.station.data = station
        new_form.direction.data = direction

        # Obter alertas relevantes para a estação
        all_alerts = Alert.get_active_alerts()
        station_alerts = []
        for alert in all_alerts:
            alert_dict = alert.to_dict()
            if not alert_dict["stations"] or station in alert_dict["stations"]:
                station_alerts.append(alert_dict)

        return render_template(
            "results.html",
            station=station,
            direction=direction,
            trains=next_trains,
            form=new_form,
            alerts=station_alerts,
        )

    return redirect(url_for("main.index"))


@main_bp.route("/reportar")
def reportar():
    form = RealTimeForm()
    return render_template("report.html", form=form)


@main_bp.route("/reportar", methods=["POST"])
def reportar_horario():
    form = RealTimeForm()
    if form.validate_on_submit():
        station = form.station.data
        direction = form.direction.data
        actual_time = form.actual_time.data

        # Mapear valores do formulário para nomes das direções no banco
        direction_mapping = {"ida": "Carlito Benevides", "volta": "Chico da Silva"}

        # Converter direção do formulário para direção do banco
        db_direction = direction_mapping.get(direction, direction)

        # Salvar no banco de dados
        save_real_time_update(station, db_direction, actual_time)

        # Atualizar modelo ML
        predictor.update_model(station, db_direction, actual_time)

        flash("Horário reportado com sucesso! Obrigado por contribuir.", "success")
        return redirect(url_for("main.reportar"))

    return render_template("report.html", form=form)


@main_bp.route("/alertas")
def alertas():
    """Página com todos os alertas da Metrofor"""
    alerts = [alert.to_dict() for alert in Alert.get_active_alerts()]
    return render_template("alerts.html", alerts=alerts)


@main_bp.route("/info-horarios")
def info_horarios():
    """Página com informações completas do banco de horários"""
    try:
        schedule_info = get_schedule_info()
        return render_template("schedule_info.html", info=schedule_info)
    except Exception as e:
        flash(f"Erro ao obter informações: {str(e)}", "error")
        return redirect(url_for("main.index"))


@main_bp.route("/docs")
def api_docs():
    """Documentação da API"""
    return render_template("docs.html")
