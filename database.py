import sqlite3
import pandas as pd
from datetime import datetime
import os
from config import METRO_DATABASE, HORARIOS_IDA_CSV, HORARIOS_VOLTA_CSV

DATABASE = METRO_DATABASE


def get_db_connection():
    """Obter conexão com o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Inicializar banco de dados e carregar dados dos CSVs"""
    conn = get_db_connection()

    # Criar tabelas
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS scheduled_times (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            horario INTEGER,
            station TEXT,
            time TEXT,
            direction TEXT
        )
    """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS real_time_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station TEXT,
            direction TEXT,
            scheduled_time TEXT,
            actual_time TIMESTAMP,
            delay_minutes INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Verificar se já existem dados programados
    cursor = conn.execute("SELECT COUNT(*) FROM scheduled_times")
    if cursor.fetchone()[0] == 0:
        load_csv_data(conn)

    conn.commit()
    conn.close()


def load_csv_data(conn):
    """Carregar dados dos arquivos CSV"""
    # Carregar horários de ida
    if os.path.exists(HORARIOS_IDA_CSV):
        df_ida = pd.read_csv(HORARIOS_IDA_CSV)
        for _, row in df_ida.iterrows():
            horario = row["Horario"]
            for station in df_ida.columns[1:]:  # Pular a coluna 'Horario'
                time = row[station]
                if pd.notna(time):  # Verificar se não é NaN
                    conn.execute(
                        "INSERT INTO scheduled_times (horario, station, time, direction) VALUES (?, ?, ?, ?)",
                        (horario, station, time, "Carlito Benevides"),
                    )

    # Carregar horários de volta
    if os.path.exists(HORARIOS_VOLTA_CSV):
        df_volta = pd.read_csv(HORARIOS_VOLTA_CSV)
        for _, row in df_volta.iterrows():
            horario = row["Horario"]
            for station in df_volta.columns[1:]:  # Pular a coluna 'Horario'
                time = row[station]
                if pd.notna(time):  # Verificar se não é NaN
                    conn.execute(
                        "INSERT INTO scheduled_times (horario, station, time, direction) VALUES (?, ?, ?, ?)",
                        (horario, station, time, "Chico da Silva"),
                    )


def get_scheduled_times(station, direction):
    """Obter horários programados para uma estação e direção"""
    conn = get_db_connection()
    cursor = conn.execute(
        "SELECT time FROM scheduled_times WHERE station = ? AND direction = ? ORDER BY time",
        (station, direction),
    )
    times = [row["time"] for row in cursor.fetchall()]
    conn.close()
    return times


def save_real_time_update(station, direction, actual_time):
    """Salvar atualização de horário real"""
    conn = get_db_connection()

    # Encontrar o horário programado mais próximo
    current_time = actual_time.time()
    cursor = conn.execute(
        "SELECT time FROM scheduled_times WHERE station = ? AND direction = ? ORDER BY time",
        (station, direction),
    )

    scheduled_times = [row["time"] for row in cursor.fetchall()]
    closest_scheduled = None
    min_diff = float("inf")

    for sched_time_str in scheduled_times:
        sched_time = datetime.strptime(sched_time_str, "%H:%M").time()
        diff = abs(
            (
                datetime.combine(datetime.today(), current_time)
                - datetime.combine(datetime.today(), sched_time)
            ).total_seconds()
        )
        if diff < min_diff:
            min_diff = diff
            closest_scheduled = sched_time_str

    if closest_scheduled:
        # Calcular atraso
        scheduled_datetime = datetime.combine(
            actual_time.date(), datetime.strptime(closest_scheduled, "%H:%M").time()
        )
        delay_minutes = int((actual_time - scheduled_datetime).total_seconds() / 60)

        conn.execute(
            """
            INSERT INTO real_time_updates 
            (station, direction, scheduled_time, actual_time, delay_minutes)
            VALUES (?, ?, ?, ?, ?)
        """,
            (station, direction, closest_scheduled, actual_time, delay_minutes),
        )

    conn.commit()
    conn.close()


def get_real_time_updates(station=None, direction=None, days=30):
    """Obter atualizações de horários reais"""
    conn = get_db_connection()

    query = """
        SELECT * FROM real_time_updates 
        WHERE created_at >= datetime('now', '-{} days')
    """.format(
        days
    )

    params = []
    if station:
        query += " AND station = ?"
        params.append(station)
    if direction:
        query += " AND direction = ?"
        params.append(direction)

    query += " ORDER BY created_at DESC"

    cursor = conn.execute(query, params)
    updates = cursor.fetchall()
    conn.close()

    return [dict(row) for row in updates]


def get_delay_statistics(station, direction):
    """Obter estatísticas de atraso para uma estação"""
    conn = get_db_connection()

    cursor = conn.execute(
        """
        SELECT 
            AVG(delay_minutes) as avg_delay,
            MIN(delay_minutes) as min_delay,
            MAX(delay_minutes) as max_delay,
            COUNT(*) as total_reports
        FROM real_time_updates 
        WHERE station = ? AND direction = ?
        AND created_at >= datetime('now', '-30 days')
    """,
        (station, direction),
    )

    result = cursor.fetchone()
    conn.close()

    if result and result["total_reports"] > 0:
        return dict(result)
    else:
        return {"avg_delay": 0, "min_delay": 0, "max_delay": 0, "total_reports": 0}
