import pandas as pd
import sqlite3
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import logger, DB_PATH
from dotenv import load_dotenv

load_dotenv()

def feature_engineering():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql('SELECT * FROM cleaned_player_stats', conn)
            if df.empty:
                logger.warning('No data available in cleaned_player_stats.')
                return

            logger.info('Loaded cleaned player stats data successfully.')

            # Ensure column types are correct
            numeric_columns = ['points', 'assists', 'rebounds']
            df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

            # Creating rolling averages for last 5 games
            df['PTS_rolling_5'] = df.groupby('player_id')['points'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
            df['AST_rolling_5'] = df.groupby('player_id')['assists'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())
            df['REB_rolling_5'] = df.groupby('player_id')['rebounds'].transform(lambda x: x.rolling(window=5, min_periods=1).mean())

            logger.info(f"Rolling averages calculated:\n{df[['PTS_rolling_5', 'AST_rolling_5', 'REB_rolling_5']].head()}")

            # Save to feature_engineered_stats table
            df.to_sql('feature_engineered_stats', conn, if_exists='replace', index=False)
            logger.info('Feature-engineered data saved to feature_engineered_stats table.')

    except sqlite3.DatabaseError as db_err:
        logger.error(f'Database error in feature_engineering: {db_err}', exc_info=True)
    except Exception as e:
        logger.error(f'Unexpected error in feature_engineering: {e}', exc_info=True)

if __name__ == '__main__':
    feature_engineering()