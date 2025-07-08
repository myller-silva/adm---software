from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    DateTimeField,
    SubmitField,
    StringField,
    TextAreaField,
    BooleanField,
    PasswordField,
)
from wtforms.validators import DataRequired, Email, Length

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


class StationForm(FlaskForm):
    station = SelectField(
        "Estação", choices=[(s, s) for s in STATIONS], validators=[DataRequired()]
    )

    direction = SelectField(
        "Sentido",
        choices=[("ida", "Carlito Benevides"), ("volta", "Chico da Silva")],
        validators=[DataRequired()],
    )

    submit = SubmitField("Consultar Horários")


class RealTimeForm(FlaskForm):
    station = SelectField(
        "Estação", choices=[(s, s) for s in STATIONS], validators=[DataRequired()]
    )

    direction = SelectField(
        "Sentido",
        choices=[("ida", "Carlito Benevides"), ("volta", "Chico da Silva")],
        validators=[DataRequired()],
    )

    actual_time = DateTimeField(
        "Horário Real de Chegada", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )

    submit = SubmitField("Reportar Horário")


class LoginForm(FlaskForm):
    username = StringField("Usuário", validators=[DataRequired()])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


class AlertForm(FlaskForm):
    title = StringField("Título", validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField(
        "Mensagem", validators=[DataRequired(), Length(min=10, max=1000)]
    )
    type = SelectField(
        "Tipo",
        choices=[("info", "Informativo"), ("warning", "Aviso"), ("danger", "Crítico")],
        validators=[DataRequired()],
    )
    priority = SelectField(
        "Prioridade",
        choices=[("low", "Baixa"), ("medium", "Média"), ("high", "Alta")],
        validators=[DataRequired()],
    )
    stations = SelectField(
        "Estações Afetadas",
        choices=[("", "Todas as estações")] + [(s, s) for s in STATIONS],
        default="",
    )
    active = BooleanField("Ativo", default=True)
    submit = SubmitField("Salvar Alerta")
