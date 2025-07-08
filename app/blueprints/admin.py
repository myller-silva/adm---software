from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from app import db
from app.models.alert import Alert
from app.models.user import User
from app.forms.forms import LoginForm, AlertForm
import json

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("admin.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Usuário ou senha inválidos.", "danger")

    return render_template("admin/login.html", form=form)


@admin_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso!", "info")
    return redirect(url_for("main.index"))


@admin_bp.route("/")
@admin_bp.route("/dashboard")
@login_required
def dashboard():
    """Dashboard principal do admin"""
    total_alerts = Alert.query.count()
    active_alerts = Alert.query.filter_by(active=True).count()
    high_priority_alerts = Alert.query.filter_by(active=True, priority="high").count()

    recent_alerts = Alert.query.order_by(Alert.created_at.desc()).limit(5).all()

    stats = {
        "total_alerts": total_alerts,
        "active_alerts": active_alerts,
        "high_priority_alerts": high_priority_alerts,
        "inactive_alerts": total_alerts - active_alerts,
    }

    return render_template(
        "admin/dashboard.html", stats=stats, recent_alerts=recent_alerts
    )


@admin_bp.route("/alerts")
@login_required
def alerts_list():
    """Lista todos os alertas"""
    page = request.args.get("page", 1, type=int)
    alerts = Alert.query.order_by(Alert.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template("admin/alerts_list.html", alerts=alerts)


@admin_bp.route("/alerts/new", methods=["GET", "POST"])
@login_required
def new_alert():
    """Criar novo alerta"""
    form = AlertForm()

    if form.validate_on_submit():
        # Processar estações afetadas
        stations_data = None
        if form.stations.data:
            stations_data = json.dumps([form.stations.data])

        alert = Alert(
            title=form.title.data,
            message=form.message.data,
            type=form.type.data,
            priority=form.priority.data,
            stations=stations_data,
            active=form.active.data,
        )

        try:
            db.session.add(alert)
            db.session.commit()
            flash("Alerta criado com sucesso!", "success")
            return redirect(url_for("admin.alerts_list"))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao salvar alerta. Tente novamente.", "danger")

    return render_template("admin/alert_form.html", form=form, title="Novo Alerta")


@admin_bp.route("/alerts/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_alert(id):
    """Editar alerta existente"""
    alert = Alert.query.get_or_404(id)
    form = AlertForm(obj=alert)

    # Pré-popular o campo de estações
    if alert.stations:
        stations_list = json.loads(alert.stations)
        if stations_list:
            form.stations.data = stations_list[0]

    if form.validate_on_submit():
        alert.title = form.title.data
        alert.message = form.message.data
        alert.type = form.type.data
        alert.priority = form.priority.data
        alert.active = form.active.data

        # Atualizar estações
        if form.stations.data:
            alert.stations = json.dumps([form.stations.data])
        else:
            alert.stations = None

        db.session.commit()

        flash("Alerta atualizado com sucesso!", "success")
        return redirect(url_for("admin.alerts_list"))

    return render_template(
        "admin/alert_form.html", form=form, alert=alert, title="Editar Alerta"
    )


@admin_bp.route("/alerts/<int:id>/delete", methods=["POST"])
@login_required
def delete_alert(id):
    """Deletar alerta"""
    alert = Alert.query.get_or_404(id)
    db.session.delete(alert)
    db.session.commit()

    flash("Alerta deletado com sucesso!", "success")
    return redirect(url_for("admin.alerts_list"))


@admin_bp.route("/alerts/<int:id>/toggle", methods=["POST"])
@login_required
def toggle_alert(id):
    """Ativar/desativar alerta"""
    alert = Alert.query.get_or_404(id)
    alert.active = not alert.active
    db.session.commit()

    status = "ativado" if alert.active else "desativado"
    flash(f"Alerta {status} com sucesso!", "success")

    return redirect(url_for("admin.alerts_list"))


@admin_bp.route("/api/stats")
@login_required
def api_stats():
    """API para estatísticas do dashboard"""
    try:
        total_alerts = Alert.query.count()
        active_alerts = Alert.query.filter_by(active=True).count()
        high_priority_alerts = Alert.query.filter_by(
            active=True, priority="high"
        ).count()

        return jsonify(
            {
                "status": "success",
                "stats": {
                    "total_alerts": total_alerts,
                    "active_alerts": active_alerts,
                    "high_priority_alerts": high_priority_alerts,
                    "inactive_alerts": total_alerts - active_alerts,
                },
            }
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
