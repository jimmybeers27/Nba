import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
import logging
from dotenv import load_dotenv  # Load environment variables

load_dotenv()  # Ensure .env variables are loaded
logging.basicConfig(level=logging.INFO)

def train_models():
    try:
        subprocess.run(['python3', 'scripts/train_xgboost.py'], check=True)  # Using subprocess for better reliability
        subprocess.run(['python3', 'scripts/train_lstm.py'], check=True)
        logging.info('Train models script executed successfully.')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error in train models script: {e}', exc_info=True)
    except Exception as e:
        logging.error(f'Unexpected error in train models script: {e}', exc_info=True)

if __name__ == '__main__':
    train_models()