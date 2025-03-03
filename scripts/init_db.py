import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sqlite3
from config.config import logger, DB_PATH # Centralized logger and DB path

def create_tables():
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)  # Ensure the data directory exists
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_stats (
                player_id INTEGER,
                player_name TEXT,
                game_date TEXT,
                points INTEGER,
                assists INTEGER,
                rebounds INTEGER,
                three_pointers INTEGER,
                turnovers INTEGER,
                plus_minus INTEGER,
                minutes_played INTEGER,
                efficiency_rating REAL,
                PRIMARY KEY (player_id, game_date)
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS betting_odds (
                player_name TEXT,
                game_date TEXT,
                prop_type TEXT,
                odds REAL,
                line REAL,
                sportsbook TEXT,
                PRIMARY KEY (player_name, game_date, prop_type, sportsbook)
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS predicted_stats (
                player_id INTEGER,
                game_date TEXT,
                xgboost_prediction REAL,
                lstm_prediction REAL,
                PRIMARY KEY (player_id, game_date)
            )
            ''')

            conn.commit()
            logger.info('Tables created successfully.')
    except sqlite3.DatabaseError as db_error:
        logger.error(f'Database error while creating tables: {db_error}', exc_info=True)
    except Exception as e:
        logger.error(f'Unexpected error creating tables: {e}', exc_info=True)

if __name__ == '__main__':
    create_tables()