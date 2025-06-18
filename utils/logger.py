import logging
import logging.handlers
from config.settings import LOGGING_SETTINGS

def setup_logger(name='PokemonBot'):
    """Setup and configure the logger for the bot."""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOGGING_SETTINGS['level']))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatter
    formatter = logging.Formatter(LOGGING_SETTINGS['format'])
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        LOGGING_SETTINGS['file'],
        maxBytes=LOGGING_SETTINGS['max_bytes'],
        backupCount=LOGGING_SETTINGS['backup_count']
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
