import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
from config.config import logger
from dotenv import load_dotenv

load_dotenv()

# Updated player list
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
    201142: 'Kevin Durant'  # Added Durant
}

def process_main():
    try:
        env = {**os.environ, 'PYTHONPATH': os.getcwd()}  # Set PYTHONPATH dynamically
        subprocess.run(['python3', '-m', 'scripts.process_data'], check=True, env=env)
        subprocess.run(['python3', '-m', 'scripts.feature_engineering'], check=True, env=env)
        logger.info('Process main script executed successfully.')
    except subprocess.CalledProcessError as e:
        logger.error(f'Error in process main script: {e}', exc_info=True)
    except Exception as e:
        logger.error(f'Unexpected error in process main script: {e}', exc_info=True)

if __name__ == '__main__':
    process_main()