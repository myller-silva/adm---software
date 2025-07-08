"""
Configurações centralizadas do projeto
"""

import os

# Diretório base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Caminhos de dados
DATA_DIR = os.path.join(BASE_DIR, "data")
HORARIOS_IDA_CSV = os.path.join(DATA_DIR, "horarios_metro_ida.csv")
HORARIOS_VOLTA_CSV = os.path.join(DATA_DIR, "horarios_metro_volta.csv")

# Caminhos de banco de dados
DATABASE_DIR = os.path.join(BASE_DIR, "database")
METRO_DATABASE = os.path.join(DATABASE_DIR, "metro_database.db")
ADMIN_DATABASE = os.path.join(DATABASE_DIR, "metro_admin.db")

# Caminhos de modelos ML
MODELS_DIR = os.path.join(BASE_DIR, "models")
METRO_MODEL_PKL = os.path.join(MODELS_DIR, "metro_model.pkl")
SCALER_PKL = os.path.join(MODELS_DIR, "scaler.pkl")
ENCODERS_PKL = os.path.join(MODELS_DIR, "encoders.pkl")

# Caminhos de templates e static
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Configurações da aplicação
SECRET_KEY = "minha-chave-ultra-secreta"
DEBUG = True

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

# Garantir que os diretórios existam
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)
