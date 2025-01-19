from app.logging_config import get_logger
from psycopg2 import pool
from app.backend.config_loader import get_config

# Get the logger
logger = get_logger(__name__)

_db_connection_pool = None

def initialize_db_connection_pool():
    global _db_connection_pool
    
    if _db_connection_pool is None:
        # Read the properties file
        config = get_config()

        db_params = {
            'host': config['db.host'],
            'port': config['db.port'],
            'database': config['db.name'],
            'user': config['db.user'],
            'password': config['db.password']
        }

        # Initialize the connection pool
        _db_connection_pool = pool.SimpleConnectionPool(
            1,  # Minimum number of connections
            config['db.pool.max-connections'],  # Maximum number of connections
            **db_params
        )

def get_connection():
    initialize_db_connection_pool()
    return _db_connection_pool.getconn()

def release_connection(conn):
    _db_connection_pool.putconn(conn)
