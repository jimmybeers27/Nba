import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from config.config import logger, DB_PATH  # Centralized logger and DB path

st.set_page_config(layout='wide', page_title='NBA Predictions Dashboard')

def load_data():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            players_df = pd.read_sql('SELECT DISTINCT player_id, player_name FROM player_stats', conn)
            return dict(zip(players_df['player_name'], players_df['player_id']))
    except Exception as e:
        logger.error(f'Error loading data: {e}', exc_info=True)
        return {}

def load_player_stats(player_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = '''SELECT game_date, points, assists, rebounds 
                       FROM player_stats WHERE player_id = ? 
                       ORDER BY game_date'''
            return pd.read_sql(query, conn, params=(player_id,))
    except Exception as e:
        logger.error(f'Error loading player stats: {e}', exc_info=True)
        return pd.DataFrame()

def load_predictions(player_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = '''SELECT game_date, xgboost_prediction, lstm_prediction 
                       FROM predicted_stats WHERE player_id = ? 
                       ORDER BY game_date'''
            return pd.read_sql(query, conn, params=(player_id,))
    except Exception as e:
        logger.error(f'Error loading predictions: {e}', exc_info=True)
        return pd.DataFrame()

player_dict = load_data()
if player_dict:
    player_name = st.sidebar.selectbox('Select Player', list(player_dict.keys()))
    player_id = player_dict[player_name]

    st.title(f'Performance and Predictions: {player_name}')

    df_stats = load_player_stats(player_id)
    df_preds = load_predictions(player_id)

    if not df_stats.empty:
        st.subheader('Player Historical Performance')
        fig, ax = plt.subplots()
        ax.plot(df_stats['game_date'], df_stats['points'], marker='o', label='Points')
        ax.plot(df_stats['game_date'], df_stats['assists'], marker='x', label='Assists')
        ax.plot(df_stats['game_date'], df_stats['rebounds'], marker='s', label='Rebounds')
        ax.set_xlabel('Game Date')
        ax.set_ylabel('Stats')
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning('No player stats available.')

    if not df_preds.empty:
        st.subheader('Model Predictions')
        fig, ax = plt.subplots()
        ax.plot(df_preds['game_date'], df_preds['xgboost_prediction'], marker='^', label='XGBoost Prediction')
        ax.plot(df_preds['game_date'], df_preds['lstm_prediction'], marker='v', label='LSTM Prediction')
        ax.set_xlabel('Game Date')
        ax.set_ylabel('Predicted Points')
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning('No predictions available.')
else:
    st.error('Failed to load player data.')