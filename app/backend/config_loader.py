from app.logging_config import get_logger
import os
import yaml 

_config = None

# Get the logger
logger = get_logger(__name__)

def load_all_configs(directory):
    global _config
    
    if _config is not None:
        return _config
    
    for filename in os.listdir(directory):
        if filename.endswith('_config.yml'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                default_config = yaml.safe_load(file)
                env = os.getenv('APP_ENV', 'dev')
                _config = default_config.get(env, default_config['default'])
                logger.info(f"Loading key value from {file_path}")

    return _config

def get_config():
    load_all_configs("./app/")
    return _config
