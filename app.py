from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime, timedelta
import sqlite3
import pandas as pd
import numpy as np
import os
import pytz
from ml_model import MetroPredictor
from database import (
    init_db,
    get_scheduled_times,
    save_real_time_update,
    get_real_time_updates,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "minha-chave-ultra-secreta"

# Configuração do fuso horário de Fortaleza
REGION_TIME_ZONE = pytz.timezone("America/Fortaleza")

def get_region_time():
    """Retorna a hora atual no fuso horário da região"""
    return datetime.now(REGION_TIME_ZONE)


# Inicializar banco de dados
init_db()

# Carregar modelo de ML
predictor = MetroPredictor()

# Lista de estações (baseada nos CSVs)
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


class StationForm(FlaskForm):
    station = SelectField(
        "Estação", choices=[(s, s) for s in STATIONS], validators=[DataRequired()]
    )
    direction = SelectField(
        "Direção",
        choices=[("ida", "Ida"), ("volta", "Volta")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Consultar Horários")


class RealTimeForm(FlaskForm):
    station = SelectField(
        "Estação", choices=[(s, s) for s in STATIONS], validators=[DataRequired()]
    )
    direction = SelectField(
        "Direção",
        choices=[("ida", "Ida"), ("volta", "Volta")],
        validators=[DataRequired()],
    )
    actual_time = DateTimeField(
        "Horário Real de Chegada", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    submit = SubmitField("Reportar Horário")


@app.route("/")
def index():
    form = StationForm()
    return render_template("index.html", form=form)


@app.route("/consultar", methods=["POST"])
def consultar_horarios():
    form = StationForm()
    if form.validate_on_submit():
        station = form.station.data
        direction = form.direction.data

        # Obter horários programados
        scheduled_times = get_scheduled_times(station, direction)

        # Obter próximos horários
        current_time = get_region_time().time()
        next_trains = []

        for time_str in scheduled_times:
            train_time = datetime.strptime(time_str, "%H:%M").time()
            if train_time > current_time:
                # Prever tempo real usando ML
                predicted_time = predictor.predict_arrival_time(
                    station, direction, time_str, get_region_time()
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

        return render_template(
            "results.html",
            station=station,
            direction=direction,
            trains=next_trains,
            form=new_form,
        )

    return redirect(url_for("index"))


@app.route("/reportar")
def reportar():
    form = RealTimeForm()
    return render_template("report.html", form=form)


@app.route("/reportar", methods=["POST"])
def reportar_horario():
    form = RealTimeForm()
    if form.validate_on_submit():
        station = form.station.data
        direction = form.direction.data
        actual_time = form.actual_time.data

        # Salvar no banco de dados
        save_real_time_update(station, direction, actual_time)

        # Atualizar modelo ML
        predictor.update_model(station, direction, actual_time)

        flash("Horário reportado com sucesso! Obrigado por contribuir.", "success")
        return redirect(url_for("reportar"))

    return render_template("report.html", form=form)


@app.route("/api/horarios/<station>/<direction>")
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


@app.route("/api/report", methods=["POST"])
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


@app.route("/docs")
def api_docs():
    """Documentação da API"""
    return render_template("docs.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
