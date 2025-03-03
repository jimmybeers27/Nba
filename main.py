import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
from config.config import logger, DB_PATH  # Importing logger and DB_PATH from config
from dotenv import load_dotenv  # Load environment variables

load_dotenv()  # Ensure environment variables are loaded

def main():
    try:
        # Use python -m to run scripts as modules within the package
        subprocess.run(['python3', '-m', 'scripts.init_db'], check=True, env={**os.environ, 'PYTHONPATH': os.getcwd()})
        subprocess.run(['python3', '-m', 'scripts.fetch_nba_stats'], check=True, env={**os.environ, 'PYTHONPATH': os.getcwd()})
        subprocess.run(['python3', '-m', 'scripts.fetch_betting_odds'], check=True, env={**os.environ, 'PYTHONPATH': os.getcwd()})
        logger.info('Main script executed successfully.')
    except subprocess.CalledProcessError as e:
        logger.error(f'Error in main script: {e}', exc_info=True)
    except Exception as e:
        logger.error(f'Unexpected error: {e}', exc_info=True)

if __name__ == '__main__':
    main()