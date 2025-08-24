import logging 
import os
from datetime import datetime

LOGS_DIR="logs"
os.makedirs(LOGS_DIR,exist_ok="True")

# logs as: log_2025-02-29.log
LOG_FILE=os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# logging as: time - INFO(/warning/error) - message 
logging.basicConfig(
    filename=LOG_FILE,
    format='%(asctime)s - %(levelname)s -%(message)s',
    level=logging.INFO
)


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

