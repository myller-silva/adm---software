from datetime import datetime
import pytz

# Configuração do fuso horário de Fortaleza
REGION_TIME_ZONE = pytz.timezone("America/Fortaleza")


def get_region_time():
    """Retorna a hora atual no fuso horário da região"""
    return datetime.now(REGION_TIME_ZONE)
