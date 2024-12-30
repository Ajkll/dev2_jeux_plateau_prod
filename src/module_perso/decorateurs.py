import logging
from functools import wraps


logger = logging.getLogger("decorator_logger")


# Configuration des logs decorateur
def log_result(func):
    """Decorateur pour enregistrer le resultat et les argument d'une methode/function dans le fichier de logs"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info(f"Method: {func.__name__}, Result: {result}")
        return result

    return wrapper
