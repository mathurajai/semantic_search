import logging
import logging.config

# Load the logging configuration
logging.config.fileConfig('./app/logging.conf')

# Get the logger
logger = logging.getLogger(__name__)

def get_logger(name):
    return logging.getLogger(name)
