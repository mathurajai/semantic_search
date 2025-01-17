from logging_config import get_logger
import psycopg2
from psycopg2 import pool
from backend.config_loader import get_config

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

def persist_records(items):
    conn = None
    try:
        # Get a connection from the pool
        conn = get_connection()
        cursor = conn.cursor()

        # Insert multiple records into the table with ON CONFLICT DO NOTHING
        insert_query = """
        INSERT INTO items (content, embedding) 
        VALUES (%s, %s) 
        ON CONFLICT (content) DO NOTHING
        """
        
        records = [item.to_tuple() for item in items]
        cursor.executemany(insert_query, records)

        # Get the number of records inserted
        inserted_records = cursor.rowcount
        
        # Commit the transaction
        conn.commit()
        logger.info(f"{inserted_records} Record(s) inserted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(f"Error while inserting: {error}")
        if conn:
            conn.rollback()
    finally:
        # Release the connection back to the pool
        if conn:
            release_connection(conn)

def cosine_search(item):
    # Get a connection from the pool
    conn = get_connection()
    cursor = conn.cursor()
    # Perform a cosine similarity search
    try:
        cursor.execute(
            """SELECT id, content, (embedding <=> %s::vector) AS cosine_similarity
               FROM items
               ORDER BY cosine_similarity LIMIT 5""",
            (item.embedding,)
        )

        # Fetch the similar results
        results = []
        for row in cursor.fetchall():
            # Only add those that are above threshold
            if row[2] < 0.7:
                results.append(f"ID: {row[0]}, CONTENT: {row[1]}, Cosine Similarity: {row[2]}")
        
        return results
    
    except Exception as e:
        logger.error(f"Error executing query {str(e)}")
    finally:
        # Close communication with the PostgreSQL database server
        cursor.close()
        release_connection(conn)