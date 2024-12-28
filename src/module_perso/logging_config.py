import logging
from logging.handlers import RotatingFileHandler
import os

# chemin pour le fichier de log
LOG_DIR = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(LOG_DIR, exist_ok=True)  # si il n'est pas la on le crer
LOG_FILE = os.path.join(LOG_DIR, "application.log")

# +- 60 KB max
MAX_LOG_SIZE = 60 * 1024
BACKUP_COUNT = 2

# Configuration globale du logging
handler = RotatingFileHandler(
    LOG_FILE, mode="a", maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[handler],
)


def get_logger(name):

    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        rotating_handler = RotatingFileHandler(
            LOG_FILE, mode="a", maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
        )
        rotating_handler.setFormatter(formatter)
        logger.addHandler(rotating_handler)
        logger.setLevel(logging.DEBUG)
    return logger
