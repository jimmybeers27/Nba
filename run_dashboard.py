import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)

def run_dashboard():
    try:
        subprocess.run(['streamlit', 'run', 'scripts/dashboard.py'], check=True)  # Using subprocess for better error handling
        logging.info('Dashboard script executed successfully.')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error running dashboard: {e}', exc_info=True)
    except Exception as e:
        logging.error(f'Unexpected error in dashboard script: {e}', exc_info=True)

if __name__ == '__main__':
    run_dashboard()
