import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables from .env file
load_dotenv()

# API Keys
ODDS_API_KEY = os.getenv('ODDS_API_KEY', 'default_api_key')  # Fallback value for API key

# Database Configurations
DB_PATH = os.getenv('DB_PATH', './nba_prediction/data/nba_stats.db')  # Default path if env not set

# Logging Configuration
LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), '../logs/project.log')

os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)  # Ensure logs directory exists

# Implement rotating log handler to prevent oversized log files
handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=5000000, backupCount=5)
logging.basicConfig(
    level=LOGGING_LEVEL,
    format=LOGGING_FORMAT,
    handlers=[handler, logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

# Model Paths with default values
XGBOOST_MODEL_PATH = os.getenv('XGBOOST_MODEL_PATH', './nba_prediction/models/xgboost_model.pkl')
LSTM_MODEL_PATH = os.getenv('LSTM_MODEL_PATH', './nba_prediction/models/lstm_model.h5')

# Other Constants
SEASON_YEAR = '2023-24'