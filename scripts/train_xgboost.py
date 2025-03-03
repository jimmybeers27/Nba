import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from config.config import logger, DB_PATH, XGBOOST_MODEL_PATH  # Centralized imports

def load_data():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql('SELECT * FROM feature_engineered_stats', conn)
            return df
    except sqlite3.DatabaseError as e:
        logger.error(f'Database error while loading data: {e}', exc_info=True)
        return pd.DataFrame()

def train_xgboost():
    try:
        df = load_data()
        if df.empty:
            logger.warning('No data available for training.')
            return

        features = ['PTS_rolling_5', 'AST_rolling_5', 'REB_rolling_5']
        X = df[features]
        y = df['points']  # Target variable

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=100)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        logger.info(f'XGBoost Model trained successfully with MSE: {mse:.4f}')

        # Save the trained model
        model.save_model(XGBOOST_MODEL_PATH)
        logger.info(f'Model saved to {XGBOOST_MODEL_PATH}')
    except Exception as e:
        logger.error(f'Error training XGBoost model: {e}', exc_info=True)

if __name__ == '__main__':
    train_xgboost()