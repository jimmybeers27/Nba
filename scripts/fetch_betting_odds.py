import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
import logging
import sqlite3
from dotenv import load_dotenv


load_dotenv()

ODDS_API_KEY = os.getenv('ODDS_API_KEY')
BASE_URL = 'https://api.the-odds-api.com/v4/sports/basketball_nba/odds'
DB_PATH = os.getenv('DB_PATH', './nba_prediction/data/nba_stats.db')

logging.basicConfig(level=logging.INFO)

def fetch_odds():
    try:
        params = {
            'apiKey': ODDS_API_KEY,
            'regions': 'us',
            'markets': 'h2h,spreads,totals',
            'oddsFormat': 'decimal',
            'dateFormat': 'iso'
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        odds_data = response.json()

        logging.info('Fetched NBA betting odds successfully.')
        logging.info(odds_data)  # Print fetched data for verification

        save_odds_to_db(odds_data)

        return odds_data
    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}', exc_info=True)
    except Exception as e:
        logging.error(f'Error fetching NBA betting odds: {e}', exc_info=True)

def save_odds_to_db(odds_data):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for game in odds_data:
                for bookmaker in game.get('bookmakers', []):
                    for market in bookmaker.get('markets', []):
                        for outcome in market.get('outcomes', []):
                            cursor.execute('''
                                INSERT OR REPLACE INTO betting_odds (player_name, game_date, prop_type, odds, line, sportsbook)
                                VALUES (?, ?, ?, ?, ?, ?)
                            ''', (
                                outcome.get('name'),
                                game.get('commence_time'),
                                market.get('key'),
                                outcome.get('price'),
                                outcome.get('point'),
                                bookmaker.get('title')
                            ))
            conn.commit()
            logging.info('Odds data saved to database successfully.')
    except sqlite3.DatabaseError as db_err:
        logging.error(f'Database error: {db_err}', exc_info=True)
    except Exception as e:
        logging.error(f'Error saving odds data: {e}', exc_info=True)

if __name__ == '__main__':
    fetch_odds()