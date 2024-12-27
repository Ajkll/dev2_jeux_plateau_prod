import logging
import os

# Chemin pour le fichier de log
LOG_DIR = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(LOG_DIR, exist_ok=True)  # Crée le répertoire des logs s'il n'existe pas
LOG_FILE = os.path.join(LOG_DIR, "application.log")

# Configuration globale du logging
logging.basicConfig(
    level=logging.DEBUG,  # Niveau global de logging
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_FILE, mode="a"
        )  # Enregistre les logs uniquement dans un fichier
    ],
)


def get_logger(name):
    """
    Renvoie un logger configuré pour l'application.

    :param name: Nom du logger (en général, __name__)
    :return: Instance de logger
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():  # Vérifie que le logger n'a pas déjà de handlers
        file_handler = logging.FileHandler(LOG_FILE, mode="a")

        # Format du log
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)

        # Ajoute les handlers au logger
        logger.addHandler(file_handler)

        # Définit le niveau du logger
        logger.setLevel(logging.DEBUG)

    return logger
