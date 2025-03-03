import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
import pandas as pd
import numpy as np
from config.config import logger, DB_PATH  # Centralized imports
from scripts.train_xgboost import train_xgboost  # Import the trained model
from scripts.train_lstm import train_lstm        # Import the trained model

def load_latest_data(player_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = '''SELECT * FROM cleaned_player_stats 
                       WHERE player_id = ? 
                       ORDER BY game_date DESC 
                       LIMIT 5'''
            df = pd.read_sql(query, conn, params=(player_id,))
            return df
    except sqlite3.DatabaseError as e:
        logger.error(f'Error loading data for player_id {player_id}: {e}', exc_info=True)
        return pd.DataFrame()

def make_predictions(model, data, model_type='XGBoost'):
    try:
        if data.empty:
            logger.warning('No data available for predictions.')
            return None
        predictions = model.predict(data)
        logger.info(f'{model_type} predictions made successfully.')
        return predictions
    except Exception as e:
        logger.error(f'Error making predictions with {model_type}: {e}', exc_info=True)
        return None

def save_predictions(player_id, predictions, model_type):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO predicted_stats (player_id, game_date, {}_prediction)
            VALUES (?, DATE('now'), ?)
            '''.format(model_type.lower()), (player_id, predictions[0]))
            conn.commit()
            logger.info(f'{model_type} predictions saved for player_id {player_id}.')
    except sqlite3.DatabaseError as db_error:
        logger.error(f'Error saving predictions: {db_error}', exc_info=True)

def daily_predictions():
    try:
        xgb_model = train_xgboost()  # Load trained XGBoost model
        lstm_model = train_lstm()    # Load trained LSTM model

        # Updated player list with LeBron James and Kevin Durant
        PLAYER_LIST = {
            203954: 'Joel Embiid',
            1626164: 'Devin Booker',
            1629630: 'Ja Morant',
            1630162: 'Anthony Edwards',
            1641703: 'Victor Wembanyama',
            200768: 'Al Horford',
            1629644: 'Jaren Jackson Jr.',
            202695: 'Klay Thompson',
            203507: 'Brook Lopez',
            1627747: 'DeAaron Fox',
            202699: 'Jrue Holiday',
            203457: 'Damian Lillard',
            203086: 'Bradley Beal',
            203496: 'Kristaps Porziņģis',
            1629645: 'Jaden McDaniels',
            1629611: 'Duncan Robinson',
            1627750: 'PJ Tucker',
            203468: 'CJ McCollum',
            203503: 'Julius Randle',
            203490: 'Tobias Harris',
            1627742: 'Josh Giddey',
            203121: 'Jonas Valančiūnas',
            1629660: 'Jalen Williams',
            1629627: 'Dereck Lively II',
            2544: 'LeBron James',  # Added LeBron
            201142: 'Kevin Durant',  # Added Durant
            203076: 'Anthony Davis',
            1626156: 'D\'Angelo Russell',
            1630558: 'Austin Reaves',
            1629060: 'Rui Hachimura',
            1629020: 'Jarred Vanderbilt',
            1629216: 'Gabe Vincent',
            1626174: 'Christian Wood',
            1629637: 'Jaxson Hayes',
            1631107: 'Max Christie',
            1629629: 'Cam Reddish',
            1627752: 'Taurean Prince',
            203999: 'Nikola Jokić',
            203507: 'Giannis Antetokounmpo',
            201939: 'Stephen Curry',
            1629029: 'Luka Dončić',
            1628369: 'Jayson Tatum'
        }

        for player_id in PLAYER_LIST:
            logger.info(f'Processing predictions for {PLAYER_LIST[player_id]}')

            data = load_latest_data(player_id)
            if data.empty:
                continue

            xgb_predictions = make_predictions(xgb_model, data[['PTS_rolling_5', 'AST_rolling_5', 'REB_rolling_5']], 'XGBoost')
            lstm_predictions = make_predictions(lstm_model, np.expand_dims(data[['PTS_rolling_5', 'AST_rolling_5', 'REB_rolling_5']].values, axis=0), 'LSTM')

            if xgb_predictions is not None:
                save_predictions(player_id, xgb_predictions, 'XGBoost')
            if lstm_predictions is not None:
                save_predictions(player_id, lstm_predictions, 'LSTM')

    except Exception as e:
        logger.error(f'Unexpected error in daily predictions: {e}', exc_info=True)

if __name__ == '__main__':
    daily_predictions()