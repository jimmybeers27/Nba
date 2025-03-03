import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import sqlite3
from nba_api.stats.endpoints import playergamelog
from config.config import logger, DB_PATH  # Use centralized logger and DB path
from dotenv import load_dotenv  # Load environment variables

load_dotenv()  # Ensure environment variables are loaded

def get_player_stats(player_id, season='2023-24'):
    try:
        game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
        df = game_log.get_data_frames()[0]
        logger.info(f'Fetched data for player_id {player_id}: {df.head()}')
        return df[['GAME_DATE', 'PTS', 'AST', 'REB', 'FG3M', 'TOV', 'PLUS_MINUS', 'MIN']]
    except Exception as e:
        logger.error(f'Error fetching stats for player_id {player_id}: {e}', exc_info=True)
        return pd.DataFrame()

def save_to_db(df, player_id, player_name):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.executemany('''
            INSERT OR REPLACE INTO player_stats (player_id, player_name, game_date, points, assists, rebounds, three_pointers, turnovers, plus_minus, minutes_played)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', [(player_id, player_name, row['GAME_DATE'], row['PTS'], row['AST'], row['REB'], row['FG3M'], row['TOV'], row['PLUS_MINUS'], row['MIN']) for _, row in df.iterrows()])
            conn.commit()
            logger.info(f'Player stats for {player_name} saved to database.')
    except sqlite3.DatabaseError as db_error:
        logger.error(f'Database error while saving stats for {player_name}: {db_error}', exc_info=True)
    except Exception as e:
        logger.error(f'Error saving stats for {player_name}: {e}', exc_info=True)

if __name__ == '__main__':
    players = {
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
    for player_id, player_name in players.items():
        logger.info(f'Fetching stats for {player_name} (ID: {player_id})')
        df = get_player_stats(player_id)
        if not df.empty:
            save_to_db(df, player_id, player_name)
        else:
            logger.warning(f'No data fetched for {player_name} (ID: {player_id})')
