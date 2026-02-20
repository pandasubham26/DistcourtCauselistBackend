import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(app):
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    app.logger.setLevel(log_level)

    # console handler
    console = logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    app.logger.addHandler(console)

    # rotating file handler
    logs_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    file_handler = RotatingFileHandler(os.path.join(logs_dir, 'app.log'), maxBytes=10_000_00, backupCount=3)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s'))
    app.logger.addHandler(file_handler)
