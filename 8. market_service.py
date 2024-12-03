
app/services/market_service.py

# BitPredector Version 2.3.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Service pour les prédictions du marché des cryptomonnaies

import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
from sklearn.model_selection import TimeSeriesSplit
from datetime import datetime
from ..models import MarketPrediction
from ..extensions import db

class MarketService:

    def predict_market(self):
        """Prédit les tendances du marché des cryptomonnaies à l'aide d'un modèle ARIMA."""
        data = self._get_historical_data()
        data_diff = data.diff().dropna()

        # Validation croisée
        tscv = TimeSeriesSplit(n_splits=5)
        rmse_list = []

        for train_index, test_index in tscv.split(data_diff):
            X_train, X_test = data_diff.iloc[train_index], data_diff.iloc[test_index]
            try:
                # Sélection automatique des paramètres
                model = auto_arima(X_train, seasonal=False, stepwise=True)
                model_fit = model.fit(X_train)

                # Faire des prédictions
                forecast = model_fit.forecast(steps=len(X_test))
                rmse = np.sqrt(np.mean((forecast - X_test) ** 2))
                rmse_list.append(rmse)
            except Exception as e:
                print(f"Erreur lors de l'entraînement du modèle : {e}")

        avg_rmse = np.mean(rmse_list) if rmse_list else None
        print(f"RMSE moyenne de la validation croisée : {avg_rmse}")

        final_model = auto_arima(data_diff, seasonal=False, stepwise=True).fit(data_diff)
        forecast_final = final_model.forecast(steps=1)[0]

        prediction = MarketPrediction(
            crypto_name='Bitcoin',
            prediction=forecast_final,
            timestamp=datetime.now(),
            arima_params=str(final_model.order)
        )

        db.session.add(prediction)
        db.session.commit()

        return prediction.to_dict()

    def _get_historical_data(self):
        """Récupère les données historiques à partir d'une API ou d'un fichier externe."""
        try:
            data = pd.read_csv('crypto_data.csv', index_col='date', parse_dates=True)
            return data
        except FileNotFoundError:
            raise Exception("Le fichier de données historiques est introuvable.")
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des données : {e}")
=======
# app/services/market_service.py

# BitPredector Version 2.3.0

# Développé par LP

# Date de la dernière mise à jour : 18/11/2024

# Description: Service pour les prédictions du marché des cryptomonnaies

import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
from sklearn.model_selection import TimeSeriesSplit
from datetime import datetime
from ..models import MarketPrediction
from ..extensions import db

class MarketService:

    def predict_market(self):
        """Prédit les tendances du marché des cryptomonnaies à l'aide d'un modèle ARIMA."""
        data = self._get_historical_data()
        data_diff = data.diff().dropna()

        # Validation croisée
        tscv = TimeSeriesSplit(n_splits=5)
        rmse_list = []

        for train_index, test_index in tscv.split(data_diff):
            X_train, X_test = data_diff.iloc[train_index], data_diff.iloc[test_index]
            try:
                # Sélection automatique des paramètres
                model = auto_arima(X_train, seasonal=False, stepwise=True)
                model_fit = model.fit(X_train)

                # Faire des prédictions
                forecast = model_fit.forecast(steps=len(X_test))
                rmse = np.sqrt(np.mean((forecast - X_test) ** 2))
                rmse_list.append(rmse)
            except Exception as e:
                print(f"Erreur lors de l'entraînement du modèle : {e}")

        avg_rmse = np.mean(rmse_list) if rmse_list else None
        print(f"RMSE moyenne de la validation croisée : {avg_rmse}")

        final_model = auto_arima(data_diff, seasonal=False, stepwise=True).fit(data_diff)
        forecast_final = final_model.forecast(steps=1)[0]

        prediction = MarketPrediction(
            crypto_name='Bitcoin',
            prediction=forecast_final,
            timestamp=datetime.now(),
            arima_params=str(final_model.order)
        )

        db.session.add(prediction)
        db.session.commit()

        return prediction.to_dict()

    def _get_historical_data(self):
        """Récupère les données historiques à partir d'une API ou d'un fichier externe."""
        try:
            data = pd.read_csv('crypto_data.csv', index_col='date', parse_dates=True)
            return data
        except FileNotFoundError:
            raise Exception("Le fichier de données historiques est introuvable.")
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des données : {e}")

