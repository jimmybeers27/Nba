import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from config.config import logger, DB_PATH, LSTM_MODEL_PATH  # Centralized imports

def load_data():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql('SELECT * FROM feature_engineered_stats', conn)
            return df
    except sqlite3.DatabaseError as e:
        logger.error(f'Database error while loading data: {e}', exc_info=True)
        return pd.DataFrame()

def prepare_sequences(df, features, target, timesteps=5):
    try:
        X, y = [], []
        for i in range(len(df) - timesteps):
            X.append(df[features].iloc[i:i+timesteps].values)
            y.append(df[target].iloc[i+timesteps])
        return np.array(X), np.array(y)
    except Exception as e:
        logger.error(f'Error preparing sequences: {e}', exc_info=True)
        return np.array([]), np.array([])

def train_lstm():
    try:
        df = load_data()
        if df.empty:
            logger.warning('No data available for training.')
            return

        features = ['PTS_rolling_5', 'AST_rolling_5', 'REB_rolling_5']
        target = 'points'

        X, y = prepare_sequences(df, features, target)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = Sequential([
            LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2]), activation='relu'),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')

        model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        logger.info(f'LSTM Model trained successfully with MSE: {mse:.4f}')

        model.save(LSTM_MODEL_PATH)
        logger.info(f'LSTM model saved to {LSTM_MODEL_PATH}')
    except Exception as e:
        logger.error(f'Error training LSTM model: {e}', exc_info=True)

if __name__ == '__main__':
    train_lstm()