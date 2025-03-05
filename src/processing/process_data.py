import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import sqlite3
from config.config import logger, DB_PATH
from dotenv import load_dotenv

load_dotenv()

def process_data():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql('SELECT * FROM player_stats', conn)
            if df.empty:
                logger.warning('No data found in player_stats table.')
                return

            logger.info('Player stats data loaded successfully.')
            logger.info(f'Initial data preview:\n{df.head()}')

            # Data cleaning and processing
            df.dropna(subset=['points', 'assists', 'rebounds', 'minutes_played'], inplace=True)
            logger.info(f'Data after dropping rows with missing key values:\n{df.head()}')

            df['efficiency'] = (df['points'] + df['assists'] + df['rebounds']) / df['minutes_played']
            logger.info(f'Data after efficiency calculation:\n{df.head()}')

            if df.empty:
                logger.warning('Processed data is empty after cleaning.')
                return

            df.to_sql('cleaned_player_stats', conn, if_exists='replace', index=False)
            logger.info('Processed data saved to cleaned_player_stats table.')

    except sqlite3.DatabaseError as db_err:
        logger.error(f'Database error in process_data: {db_err}', exc_info=True)
    except Exception as e:
        logger.error(f'Unexpected error in process_data: {e}', exc_info=True)

if __name__ == '__main__':
    process_data()
