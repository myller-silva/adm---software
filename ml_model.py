import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import pickle
import os
from database import get_real_time_updates, get_delay_statistics


class MetroPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.station_encoder = LabelEncoder()
        self.direction_encoder = LabelEncoder()
        self.is_trained = False
        self.model_path = "metro_model.pkl"
        self.scaler_path = "scaler.pkl"
        self.encoders_path = "encoders.pkl"

        # Lista de estações para o encoder
        self.stations = [
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

        self.directions = ["ida", "volta"]

        # Inicializar encoders
        self.station_encoder.fit(self.stations)
        self.direction_encoder.fit(self.directions)

        # Tentar carregar modelo existente
        self.load_model()

        # Se não houver modelo, criar um básico
        if not self.is_trained:
            self.create_basic_model()

    def create_basic_model(self):
        """Criar modelo Random Forest básico"""
        # Criar modelo
        self.model = RandomForestRegressor(
            n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
        )

        # Treinar com dados sintéticos básicos se não houver dados reais
        self._train_with_synthetic_data()

    def _train_with_synthetic_data(self):
        """Treinar com dados sintéticos básicos"""
        print("Treinando modelo com dados sintéticos...")

        # Gerar dados sintéticos para treinamento inicial
        n_samples = 1000

        # Features: [station_encoded, direction_encoded, hour, minute, day_of_week, is_peak_hour]
        X_synthetic = []
        y_synthetic = []

        for _ in range(n_samples):
            station_idx = np.random.choice(len(self.stations))
            direction_idx = np.random.choice(len(self.directions))
            hour = np.random.randint(5, 24)
            minute = np.random.choice([0, 15, 30, 45])
            day_of_week = np.random.randint(0, 7)
            is_peak_hour = 1 if hour in [7, 8, 17, 18, 19] else 0

            # Simular atraso baseado em padrões típicos
            base_delay = 0
            if is_peak_hour:
                base_delay += np.random.normal(3, 2)  # Mais atraso em horário de pico
            if day_of_week in [0, 6]:  # Segunda e domingo
                base_delay += np.random.normal(1, 1)

            delay = max(0, base_delay + np.random.normal(0, 1))

            X_synthetic.append(
                [station_idx, direction_idx, hour, minute, day_of_week, is_peak_hour]
            )
            y_synthetic.append(delay)

        X_synthetic = np.array(X_synthetic)
        y_synthetic = np.array(y_synthetic)

        # Normalizar features
        X_scaled = self.scaler.fit_transform(X_synthetic)

        # Treinar modelo
        self.model.fit(X_scaled, y_synthetic)

        self.is_trained = True
        self.save_model()
        print("Modelo treinado com sucesso!")

    def extract_features(self, station, direction, scheduled_time, current_datetime):
        """Extrair features para predição"""
        # Converter horário programado
        if isinstance(scheduled_time, str):
            scheduled_dt = datetime.strptime(scheduled_time, "%H:%M").replace(
                year=current_datetime.year,
                month=current_datetime.month,
                day=current_datetime.day,
            )
        else:
            scheduled_dt = scheduled_time

        # Encodar estação e direção
        station_encoded = self.station_encoder.transform([station])[0]
        direction_encoded = self.direction_encoder.transform([direction])[0]

        # Extrair características temporais
        hour = scheduled_dt.hour
        minute = scheduled_dt.minute
        day_of_week = scheduled_dt.weekday()
        is_peak_hour = 1 if hour in [7, 8, 17, 18, 19] else 0

        return np.array(
            [
                [
                    station_encoded,
                    direction_encoded,
                    hour,
                    minute,
                    day_of_week,
                    is_peak_hour,
                ]
            ]
        )

    def predict_arrival_time(
        self, station, direction, scheduled_time, current_datetime
    ):
        """Predizer horário real de chegada"""
        try:
            # Extrair features
            features = self.extract_features(
                station, direction, scheduled_time, current_datetime
            )

            # Normalizar
            features_scaled = self.scaler.transform(features)

            # Predizer atraso
            predicted_delay = self.model.predict(features_scaled)[0]

            # Garantir que o atraso não seja negativo
            predicted_delay = max(0, predicted_delay)

            # Calcular horário previsto
            if isinstance(scheduled_time, str):
                scheduled_dt = datetime.strptime(scheduled_time, "%H:%M").replace(
                    year=current_datetime.year,
                    month=current_datetime.month,
                    day=current_datetime.day,
                )
            else:
                scheduled_dt = scheduled_time

            predicted_time = scheduled_dt + timedelta(minutes=predicted_delay)

            return predicted_time

        except Exception as e:
            print(f"Erro na predição: {e}")
            # Em caso de erro, retornar horário programado
            if isinstance(scheduled_time, str):
                return datetime.strptime(scheduled_time, "%H:%M").replace(
                    year=current_datetime.year,
                    month=current_datetime.month,
                    day=current_datetime.day,
                )
            return scheduled_time

    def update_model(self, station, direction, actual_time):
        """Atualizar modelo com novos dados"""
        try:
            # Obter dados históricos
            updates = get_real_time_updates(station, direction, days=30)

            if len(updates) < 10:  # Poucos dados para re-treinar
                return

            # Preparar dados de treinamento
            X_new = []
            y_new = []

            for update in updates:
                scheduled_time = update["scheduled_time"]
                delay = update["delay_minutes"]
                created_at = datetime.fromisoformat(update["created_at"])

                features = self.extract_features(
                    station, direction, scheduled_time, created_at
                )
                X_new.append(features[0])
                y_new.append(delay)

            if len(X_new) > 0:
                X_new = np.array(X_new)
                y_new = np.array(y_new)

                # Normalizar
                X_scaled = self.scaler.transform(X_new)

                # Re-treinar modelo com novos dados
                self.model.fit(X_scaled, y_new)

                # Salvar modelo atualizado
                self.save_model()
                print(f"Modelo atualizado com {len(X_new)} novos registros")

        except Exception as e:
            print(f"Erro ao atualizar modelo: {e}")

    def save_model(self):
        """Salvar modelo e preprocessadores"""
        try:
            if self.model:
                with open(self.model_path, "wb") as f:
                    pickle.dump(self.model, f)

            with open(self.scaler_path, "wb") as f:
                pickle.dump(self.scaler, f)

            with open(self.encoders_path, "wb") as f:
                pickle.dump(
                    {
                        "station_encoder": self.station_encoder,
                        "direction_encoder": self.direction_encoder,
                    },
                    f,
                )

        except Exception as e:
            print(f"Erro ao salvar modelo: {e}")

    def load_model(self):
        """Carregar modelo e preprocessadores"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
                self.is_trained = True
                print("Modelo carregado do disco")

            if os.path.exists(self.scaler_path):
                with open(self.scaler_path, "rb") as f:
                    self.scaler = pickle.load(f)

            if os.path.exists(self.encoders_path):
                with open(self.encoders_path, "rb") as f:
                    encoders = pickle.load(f)
                    self.station_encoder = encoders["station_encoder"]
                    self.direction_encoder = encoders["direction_encoder"]

        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            self.is_trained = False

    def get_model_info(self):
        """Obter informações sobre o modelo"""
        return {
            "is_trained": self.is_trained,
            "model_exists": self.model is not None,
            "model_type": "RandomForestRegressor",
            "stations_count": len(self.stations),
            "directions_count": len(self.directions),
            "features": [
                "station",
                "direction",
                "hour",
                "minute",
                "day_of_week",
                "is_peak_hour",
            ],
        }
